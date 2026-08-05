#!/usr/bin/env python3
"""
Production Deployment Example — Integration Engine v2.0.0

Demonstrates production-ready deployment with comprehensive configuration,
monitoring, and error handling.
"""

import logging
from integration_engine import IntegrationEngine

# Configure structured logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # In production, also log to file:
        # logging.FileHandler('integration_engine.log')
    ]
)

logger = logging.getLogger(__name__)


class ProductionIntegrationService:
    """
    Production-ready integration service with comprehensive configuration.
    """
    
    def __init__(self, cache_size=512, log_level=logging.INFO):
        """
        Initialize production integration service.
        
        Args:
            cache_size: Size of LRU cache (default: 512 for production)
            log_level: Logging level (default: INFO)
        """
        logger.info("Initializing Production Integration Service")
        
        self.engine = IntegrationEngine(
            enable_cache=True,
            enable_telemetry=True,
            cache_size=cache_size,
            log_level=log_level,
        )
        
        logger.info(f"Engine configured: cache_size={cache_size}, telemetry=enabled")
    
    def handle_request(self, patterns, request_id=None):
        """
        Handle an integration request with full error handling and logging.
        
        Args:
            patterns: Pattern data to integrate
            request_id: Optional request identifier for tracing
            
        Returns:
            Integration result or error response
        """
        req_id = request_id or "unknown"
        logger.info(f"[{req_id}] Processing integration request with {len(patterns)} patterns")
        
        try:
            # Execute integration
            result = self.engine.integrate(patterns)
            
            # Log success
            logger.info(f"[{req_id}] Integration successful")
            
            # Return result with metadata
            return {
                "status": "success",
                "request_id": req_id,
                "result": result,
                "cache_stats": self.engine.get_cache_stats(),
            }
            
        except ValueError as e:
            logger.error(f"[{req_id}] Validation error: {e}")
            return {
                "status": "error",
                "request_id": req_id,
                "error": "validation_error",
                "message": str(e),
            }
            
        except Exception as e:
            logger.exception(f"[{req_id}] Unexpected error during integration")
            return {
                "status": "error",
                "request_id": req_id,
                "error": "internal_error",
                "message": "An unexpected error occurred",
            }
    
    def get_health_status(self):
        """
        Get service health status for monitoring.
        
        Returns:
            Health status dict with metrics
        """
        metrics = self.engine.get_metrics()
        cache_stats = self.engine.get_cache_stats()
        
        # Determine health based on error rate
        error_rate = metrics.get('error_rate', 0)
        health = "healthy" if error_rate < 0.05 else "degraded"
        
        return {
            "status": health,
            "metrics": metrics,
            "cache": cache_stats,
        }
    
    def shutdown(self):
        """Graceful shutdown with final statistics."""
        logger.info("Shutting down Integration Service")
        
        final_metrics = self.engine.get_metrics()
        final_cache = self.engine.get_cache_stats()
        
        logger.info(f"Final metrics: {final_metrics}")
        logger.info(f"Final cache stats: {final_cache}")
        logger.info("Shutdown complete")


# Example production usage
def main():
    """Main production entry point."""
    print("\n" + "=" * 60)
    print("PRODUCTION INTEGRATION SERVICE — DEMONSTRATION")
    print("=" * 60 + "\n")
    
    # Initialize service
    service = ProductionIntegrationService(cache_size=512)
    
    # Simulate production requests
    requests = [
        {
            "request_id": "req_001",
            "patterns": [
                {"id": "p1", "type": "transformation", "data": [1, 2, 3]},
                {"id": "p2", "type": "harmonic", "data": [4, 5, 6]},
            ]
        },
        {
            "request_id": "req_002",
            "patterns": [
                {"id": "p3", "type": "recursive", "data": [7, 8, 9]},
            ]
        },
        {
            "request_id": "req_003",
            "patterns": [
                {"id": "p1", "type": "transformation", "data": [1, 2, 3]},  # Duplicate for cache
            ]
        },
    ]
    
    # Process requests
    results = []
    for req in requests:
        result = service.handle_request(
            patterns=req["patterns"],
            request_id=req["request_id"]
        )
        results.append(result)
        print(f"Request {req['request_id']}: {result['status']}")
    
    # Check health
    print("\n" + "=" * 60)
    print("HEALTH STATUS")
    print("=" * 60)
    health = service.get_health_status()
    print(f"Status: {health['status']}")
    print(f"Metrics: {health['metrics']}")
    print(f"Cache: {health['cache']}")
    
    # Graceful shutdown
    print("\n" + "=" * 60)
    print("SHUTDOWN")
    print("=" * 60)
    service.shutdown()


if __name__ == "__main__":
    main()
