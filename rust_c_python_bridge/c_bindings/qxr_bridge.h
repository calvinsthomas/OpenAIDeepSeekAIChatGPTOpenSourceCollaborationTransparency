/**
 * QXR Bridge C Header
 * 
 * C API for the Rust-C-Python bridge providing high-performance
 * integration for the QXR social media system.
 */

#ifndef QXR_BRIDGE_H
#define QXR_BRIDGE_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>
#include <stdint.h>

// Forward declaration of opaque bridge type
typedef struct QXRBridge QXRBridge;

// Research data structure (matches Rust definition)
typedef struct {
    int32_t signals;
    int32_t opportunities;
    double signal_strength;
    double price_range_min;
    double price_range_max;
    int64_t max_liquidity;
    size_t strategy_len;
    char* strategy_ptr;
    size_t timeframe_len;
    char* timeframe_ptr;
} QXRResearchData;

// Social media post structure
typedef struct {
    size_t platform_len;
    char* platform_ptr;
    size_t content_len;
    char* content_ptr;
    size_t hashtags_count;
    char** hashtags_ptr;
    double engagement_score;
} QXRSocialPost;

// Bridge lifecycle functions
QXRBridge* qxr_bridge_create(void);
void qxr_bridge_destroy(QXRBridge* bridge);

// Core processing functions
double qxr_bridge_process_data(QXRBridge* bridge, const QXRResearchData* data);
int qxr_bridge_generate_content(
    QXRBridge* bridge,
    const QXRResearchData* data,
    const char* platform,
    char* output_buffer,
    size_t buffer_size
);

// Batch processing
int qxr_bridge_batch_process(
    QXRBridge* bridge,
    const QXRResearchData* data_array,
    size_t data_count,
    double* results
);

// Memory management
char* qxr_bridge_alloc_string(size_t len);
void qxr_bridge_free_string(char* ptr);

// Utility functions
const char* qxr_bridge_version(void);

// Python integration helpers
typedef struct {
    QXRBridge* bridge;
    char* error_message;
    int last_error_code;
} QXRBridgeContext;

QXRBridgeContext* qxr_bridge_create_context(void);
void qxr_bridge_destroy_context(QXRBridgeContext* ctx);
int qxr_bridge_set_error(QXRBridgeContext* ctx, int code, const char* message);
const char* qxr_bridge_get_error(QXRBridgeContext* ctx);

#ifdef __cplusplus
}
#endif

#endif // QXR_BRIDGE_H