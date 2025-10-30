<?php
/**
 * @package     UHA Component
 * @subpackage  com_uha
 *
 * @copyright   (C) 2025 All Your Baseline LLC
 * @license     Proprietary
 */

namespace AllYourBaseline\Component\Uha\Site\Helper;

defined('_JEXEC') or die;

use Joomla\CMS\Http\HttpFactory;
use Joomla\CMS\Log\Log;
use Joomla\CMS\Factory;

/**
 * API Helper class - Proxy for Django backend API
 *
 * Security: All API calls go through this PHP proxy to prevent
 * exposing Django endpoint URLs to frontend JavaScript
 *
 * @since  1.0.0
 */
class ApiHelper
{
    /**
     * Django API base URL (from component configuration)
     *
     * @var string
     */
    private static $apiEndpoint = 'https://got.gitgap.org/api';

    /**
     * API request timeout in seconds
     *
     * @var int
     */
    private static $timeout = 30;

    /**
     * Initialize API settings from component configuration
     *
     * @return void
     */
    private static function init()
    {
        $db = Factory::getDbo();
        $query = $db->getQuery(true)
            ->select($db->quoteName(['config_key', 'config_value']))
            ->from($db->quoteName('#__uha_config'))
            ->where($db->quoteName('config_key') . ' IN (' .
                $db->quote('django_api_endpoint') . ',' .
                $db->quote('api_timeout') . ')');

        $db->setQuery($query);
        $config = $db->loadAssocList('config_key');

        if (!empty($config['django_api_endpoint']['config_value'])) {
            self::$apiEndpoint = $config['django_api_endpoint']['config_value'];
        }

        if (!empty($config['api_timeout']['config_value'])) {
            self::$timeout = (int) $config['api_timeout']['config_value'];
        }
    }

    /**
     * Request new API token from Django
     *
     * @param   array  $userData  User data (name, email, institution, etc.)
     *
     * @return  object|false  Response object or false on failure
     *
     * @since   1.0.0
     */
    public static function requestToken($userData)
    {
        self::init();

        $data = [
            'name'         => $userData['name'] ?? '',
            'institution'  => $userData['institution'] ?? '',
            'email'        => $userData['email'] ?? '',
            'access_tier'  => $userData['access_tier'] ?? 'academic',
            'use_case'     => $userData['use_case'] ?? '',
            'daily_limit'  => $userData['daily_limit'] ?? 1000
        ];

        $response = self::post('/request-token', $data);

        if ($response && !empty($response->token)) {
            self::log('Token requested successfully for ' . $data['email']);
            return $response;
        }

        self::log('Token request failed for ' . $data['email'], 'error');
        return false;
    }

    /**
     * Get token usage statistics from Django
     *
     * @param   string  $token  API token
     *
     * @return  object|false  Usage stats or false on failure
     *
     * @since   1.0.0
     */
    public static function getUsageStats($token)
    {
        self::init();

        $headers = [
            'Authorization' => 'Token ' . $token
        ];

        $response = self::get('/token/usage', $headers);

        if ($response) {
            return $response;
        }

        return false;
    }

    /**
     * Execute multi-resolution proof via Django API
     *
     * @param   string  $token  API token
     * @param   array   $data   Proof parameters
     *
     * @return  object|false  Proof results or false on failure
     *
     * @since   1.0.0
     */
    public static function executeProof($token, $data)
    {
        self::init();

        $headers = [
            'Authorization' => 'Token ' . $token,
            'Content-Type'  => 'application/json'
        ];

        $response = self::post('/v1/merge/multiresolution', $data, $headers);

        if ($response) {
            self::log('Proof executed successfully');
            return $response;
        }

        self::log('Proof execution failed', 'error');
        return false;
    }

    /**
     * Validate API token (check if it's active)
     *
     * @param   string  $token  API token to validate
     *
     * @return  bool  True if valid, false otherwise
     *
     * @since   1.0.0
     */
    public static function validateToken($token)
    {
        self::init();

        $headers = [
            'Authorization' => 'Token ' . $token
        ];

        $response = self::get('/token/validate', $headers);

        return ($response && !empty($response->valid));
    }

    /**
     * POST request to Django API
     *
     * @param   string  $endpoint  API endpoint path
     * @param   array   $data      Request data
     * @param   array   $headers   Optional additional headers
     *
     * @return  object|false  Response body or false on failure
     *
     * @since   1.0.0
     */
    private static function post($endpoint, $data, $headers = [])
    {
        try {
            $url = self::$apiEndpoint . $endpoint;

            // Get Joomla HTTP client
            $http = HttpFactory::getHttp();

            // Prepare headers
            $defaultHeaders = [
                'Content-Type' => 'application/json',
                'User-Agent'   => 'UHA-Joomla-Component/1.0'
            ];
            $headers = array_merge($defaultHeaders, $headers);

            // Make POST request
            $response = $http->post(
                $url,
                json_encode($data),
                $headers,
                self::$timeout
            );

            // Check HTTP status
            if ($response->code >= 200 && $response->code < 300) {
                $body = json_decode($response->body);

                if (json_last_error() === JSON_ERROR_NONE) {
                    return $body;
                }

                self::log('Invalid JSON response from Django API', 'error');
                return false;
            }

            self::log('Django API returned HTTP ' . $response->code . ': ' . $response->body, 'error');
            return false;

        } catch (\Exception $e) {
            self::log('Exception in API POST: ' . $e->getMessage(), 'error');
            return false;
        }
    }

    /**
     * GET request to Django API
     *
     * @param   string  $endpoint  API endpoint path
     * @param   array   $headers   Optional headers
     *
     * @return  object|false  Response body or false on failure
     *
     * @since   1.0.0
     */
    private static function get($endpoint, $headers = [])
    {
        try {
            $url = self::$apiEndpoint . $endpoint;

            // Get Joomla HTTP client
            $http = HttpFactory::getHttp();

            // Prepare headers
            $defaultHeaders = [
                'Accept'     => 'application/json',
                'User-Agent' => 'UHA-Joomla-Component/1.0'
            ];
            $headers = array_merge($defaultHeaders, $headers);

            // Make GET request
            $response = $http->get($url, $headers, self::$timeout);

            // Check HTTP status
            if ($response->code >= 200 && $response->code < 300) {
                $body = json_decode($response->body);

                if (json_last_error() === JSON_ERROR_NONE) {
                    return $body;
                }

                self::log('Invalid JSON response from Django API', 'error');
                return false;
            }

            self::log('Django API returned HTTP ' . $response->code, 'error');
            return false;

        } catch (\Exception $e) {
            self::log('Exception in API GET: ' . $e->getMessage(), 'error');
            return false;
        }
    }

    /**
     * Log API activity
     *
     * @param   string  $message  Log message
     * @param   string  $level    Log level (info, warning, error)
     *
     * @return  void
     *
     * @since   1.0.0
     */
    private static function log($message, $level = 'info')
    {
        Log::add($message, Log::INFO, 'com_uha');
    }

    /**
     * Get API endpoint URL (for display purposes only)
     *
     * @return  string  Django API endpoint
     *
     * @since   1.0.0
     */
    public static function getEndpoint()
    {
        self::init();
        return self::$apiEndpoint;
    }
}
