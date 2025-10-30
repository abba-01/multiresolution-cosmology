<?php
/**
 * @package     UHA Component
 * @subpackage  com_uha
 *
 * @copyright   (C) 2025 All Your Baseline LLC
 * @license     Proprietary
 */

defined('_JEXEC') or die;

use Joomla\CMS\Dispatcher\ComponentDispatcherFactoryInterface;
use Joomla\CMS\Extension\ComponentInterface;
use Joomla\CMS\Extension\Service\Provider\ComponentDispatcherFactory;
use Joomla\CMS\Extension\Service\Provider\MVCFactory;
use Joomla\CMS\HTML\Registry;
use Joomla\CMS\MVC\Factory\MVCFactoryInterface;
use Joomla\DI\Container;
use Joomla\DI\ServiceProviderInterface;
use AllYourBaseline\Component\Uha\Administrator\Extension\UhaComponent;

/**
 * The UHA component service provider.
 *
 * @since  1.0.0
 */
return new class implements ServiceProviderInterface
{
    /**
     * Registers the service provider with a DI container.
     *
     * @param   Container  $container  The DI container.
     *
     * @return  void
     *
     * @since   1.0.0
     */
    public function register(Container $container)
    {
        $container->registerServiceProvider(new MVCFactory('\\AllYourBaseline\\Component\\Uha'));
        $container->registerServiceProvider(new ComponentDispatcherFactory('\\AllYourBaseline\\Component\\Uha'));

        $container->set(
            ComponentInterface::class,
            function (Container $container) {
                $component = new UhaComponent($container->get(ComponentDispatcherFactoryInterface::class));
                $component->setRegistry($container->get(Registry::class));
                $component->setMVCFactory($container->get(MVCFactoryInterface::class));

                return $component;
            }
        );
    }
};
