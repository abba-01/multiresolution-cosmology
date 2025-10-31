"""
API Configuration
==================

Single source of truth for API endpoints, timeouts, rate limits,
and authentication configuration.

Author: Eric D. Martin
Date: 2025-10-30
License: MIT
"""

import os
from typing import Dict, Optional
from dataclasses import dataclass


# ============================================================================
# API Endpoints
# ============================================================================

# Base URLs
API_BASE_URL = "https://got.gitgap.org"
API_BASE_URL_PROD = "https://api.aybllc.org"

# Specific endpoints
TOKEN_ENDPOINT = f"{API_BASE_URL}/api/request-token"
UHA_ENCODE_ENDPOINT = f"{API_BASE_URL}/uha/encode"
MULTIRESOLUTION_ENDPOINT = f"{API_BASE_URL}/v1/merge/multiresolution"

# Production endpoints
TOKEN_ENDPOINT_PROD = f"{API_BASE_URL_PROD}/api/request-token"
UHA_ENCODE_ENDPOINT_PROD = f"{API_BASE_URL_PROD}/v1/uha/encode"
MULTIRESOLUTION_ENDPOINT_PROD = f"{API_BASE_URL_PROD}/v1/merge/multiresolution"


# ============================================================================
# Rate Limiting
# ============================================================================

# API key request rate limit (HARD-CODED MAXIMUM)
API_KEY_REQUEST_INTERVAL_SECONDS = 60  # 1 request per minute

# General API call rate limits (calls per minute)
RATE_LIMIT_FREE_TIER = 10
RATE_LIMIT_ACADEMIC_TIER = 60
RATE_LIMIT_PREMIUM_TIER = 600


# ============================================================================
# Timeouts
# ============================================================================

# Connection timeout (seconds)
CONNECTION_TIMEOUT_SECONDS = 30

# Read timeout (seconds)
READ_TIMEOUT_SECONDS = 60

# Combined timeout tuple for requests library
REQUEST_TIMEOUT = (CONNECTION_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS)


# ============================================================================
# Retry Configuration
# ============================================================================

# Maximum retry attempts for failed requests
MAX_RETRY_ATTEMPTS = 3

# Base delay for exponential backoff (seconds)
RETRY_BASE_DELAY_SECONDS = 2.0

# Maximum delay between retries (seconds)
RETRY_MAX_DELAY_SECONDS = 60.0


# ============================================================================
# User Configuration (Environment Variables)
# ============================================================================

@dataclass
class UserConfig:
    """User API configuration loaded from environment variables."""
    name: str
    institution: str
    email: str
    access_tier: str
    daily_limit: int
    use_case: str = "Research"

    @classmethod
    def from_env(cls) -> 'UserConfig':
        """
        Load user configuration from environment variables.

        Required environment variables:
            UHA_EMAIL: User email address (required)

        Optional environment variables:
            UHA_USER_NAME: User full name (default: "Research User")
            UHA_INSTITUTION: Institution name (default: "Academic")
            UHA_ACCESS_TIER: Access tier (default: "academic")
            UHA_DAILY_LIMIT: Daily API call limit (default: 1000)
            UHA_USE_CASE: Use case description (default: "Research")

        Returns:
            UserConfig instance

        Raises:
            ValueError: If required environment variables are missing
        """
        email = os.getenv("UHA_EMAIL")
        if not email:
            raise ValueError(
                "UHA_EMAIL environment variable is required. "
                "Please set it in your .env file or environment."
            )

        return cls(
            name=os.getenv("UHA_USER_NAME", "Research User"),
            institution=os.getenv("UHA_INSTITUTION", "Academic"),
            email=email,
            access_tier=os.getenv("UHA_ACCESS_TIER", "academic"),
            daily_limit=int(os.getenv("UHA_DAILY_LIMIT", "1000")),
            use_case=os.getenv("UHA_USE_CASE", "Research")
        )

    def to_dict(self) -> Dict[str, any]:
        """Convert to dictionary for API requests."""
        return {
            "name": self.name,
            "institution": self.institution,
            "email": self.email,
            "access_tier": self.access_tier,
            "daily_limit": self.daily_limit,
            "use_case": self.use_case
        }


# ============================================================================
# Offline/Demo Mode
# ============================================================================

# Enable offline mode by default for development
# Set to False to use real API
OFFLINE_MODE = bool(os.getenv("UHA_OFFLINE_MODE", "True").lower() in ('true', '1', 'yes'))

# Demo API key for offline mode
DEMO_API_KEY = "DEMO_API_KEY_OFFLINE_MODE"

# Demo mode notice
DEMO_MODE_NOTICE = "DEMO MODE: Using simulated corrections (API unavailable)"


# ============================================================================
# API Response Limits
# ============================================================================

# Maximum array sizes in API requests/responses
MAX_ARRAY_SIZE = 50000

# Maximum JSON response size (bytes)
MAX_RESPONSE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


# ============================================================================
# Helper Functions
# ============================================================================

def get_user_config() -> UserConfig:
    """
    Get user configuration from environment.

    Returns:
        UserConfig instance

    Raises:
        ValueError: If required environment variables missing
    """
    return UserConfig.from_env()


def get_api_endpoints(production: bool = False) -> Dict[str, str]:
    """
    Get API endpoint URLs.

    Args:
        production: If True, use production endpoints

    Returns:
        Dictionary with endpoint URLs
    """
    if production:
        return {
            'base_url': API_BASE_URL_PROD,
            'token': TOKEN_ENDPOINT_PROD,
            'uha_encode': UHA_ENCODE_ENDPOINT_PROD,
            'multiresolution': MULTIRESOLUTION_ENDPOINT_PROD
        }
    else:
        return {
            'base_url': API_BASE_URL,
            'token': TOKEN_ENDPOINT,
            'uha_encode': UHA_ENCODE_ENDPOINT,
            'multiresolution': MULTIRESOLUTION_ENDPOINT
        }


def get_rate_limit(tier: str) -> int:
    """
    Get rate limit for access tier.

    Args:
        tier: Access tier ('free', 'academic', or 'premium')

    Returns:
        Rate limit in calls per minute

    Raises:
        ValueError: If tier not recognized
    """
    limits = {
        'free': RATE_LIMIT_FREE_TIER,
        'academic': RATE_LIMIT_ACADEMIC_TIER,
        'premium': RATE_LIMIT_PREMIUM_TIER
    }

    tier_lower = tier.lower()
    if tier_lower not in limits:
        raise ValueError(
            f"Unknown access tier: {tier}. "
            f"Valid options: {', '.join(limits.keys())}"
        )

    return limits[tier_lower]


def is_offline_mode() -> bool:
    """Check if offline mode is enabled."""
    return OFFLINE_MODE


def get_demo_notice() -> str:
    """Get demo mode notice message."""
    return DEMO_MODE_NOTICE if OFFLINE_MODE else ""


# ============================================================================
# Environment Variable Loading
# ============================================================================

def load_dotenv_if_available():
    """
    Load .env file if python-dotenv is installed.

    This is a convenience function that will load environment variables
    from a .env file if the python-dotenv package is available.
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # python-dotenv not installed, environment variables must be set manually
        pass


# Auto-load .env on import if available
load_dotenv_if_available()


# ============================================================================
# Configuration Summary
# ============================================================================

def print_config_summary():
    """Print current API configuration."""
    print("\n" + "="*80)
    print("API CONFIGURATION SUMMARY")
    print("="*80)

    print(f"\nMode: {'OFFLINE (Demo)' if OFFLINE_MODE else 'ONLINE (Live API)'}")

    endpoints = get_api_endpoints(production=False)
    print(f"\nEndpoints:")
    print(f"  Base URL:          {endpoints['base_url']}")
    print(f"  Token:             {endpoints['token']}")
    print(f"  UHA Encode:        {endpoints['uha_encode']}")
    print(f"  Multi-resolution:  {endpoints['multiresolution']}")

    print(f"\nRate Limiting:")
    print(f"  Token requests:    1 per {API_KEY_REQUEST_INTERVAL_SECONDS}s")
    print(f"  Free tier:         {RATE_LIMIT_FREE_TIER} calls/min")
    print(f"  Academic tier:     {RATE_LIMIT_ACADEMIC_TIER} calls/min")
    print(f"  Premium tier:      {RATE_LIMIT_PREMIUM_TIER} calls/min")

    print(f"\nTimeouts:")
    print(f"  Connection:        {CONNECTION_TIMEOUT_SECONDS}s")
    print(f"  Read:              {READ_TIMEOUT_SECONDS}s")

    print(f"\nRetry:")
    print(f"  Max attempts:      {MAX_RETRY_ATTEMPTS}")
    print(f"  Base delay:        {RETRY_BASE_DELAY_SECONDS}s")
    print(f"  Max delay:         {RETRY_MAX_DELAY_SECONDS}s")

    try:
        user_config = get_user_config()
        print(f"\nUser Configuration:")
        print(f"  Name:              {user_config.name}")
        print(f"  Institution:       {user_config.institution}")
        print(f"  Email:             {user_config.email}")
        print(f"  Access tier:       {user_config.access_tier}")
        print(f"  Daily limit:       {user_config.daily_limit}")
    except ValueError as e:
        print(f"\nUser Configuration: Not loaded ({e})")

    print("="*80 + "\n")


# ============================================================================
# Validation
# ============================================================================

# Verify rate limits are positive
assert API_KEY_REQUEST_INTERVAL_SECONDS > 0, "API key interval must be positive"
assert RATE_LIMIT_FREE_TIER > 0, "Free tier rate limit must be positive"
assert RATE_LIMIT_ACADEMIC_TIER > RATE_LIMIT_FREE_TIER, "Academic tier should be higher than free"
assert RATE_LIMIT_PREMIUM_TIER > RATE_LIMIT_ACADEMIC_TIER, "Premium tier should be highest"

# Verify timeouts are reasonable
assert 0 < CONNECTION_TIMEOUT_SECONDS <= 300, "Connection timeout should be 0-300s"
assert 0 < READ_TIMEOUT_SECONDS <= 600, "Read timeout should be 0-600s"

# Verify retry configuration
assert MAX_RETRY_ATTEMPTS > 0, "Must allow at least one retry attempt"
assert RETRY_BASE_DELAY_SECONDS > 0, "Retry base delay must be positive"
assert RETRY_MAX_DELAY_SECONDS >= RETRY_BASE_DELAY_SECONDS, "Max delay must be >= base delay"
