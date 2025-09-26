/**
 * QXR Bridge C Wrapper
 * 
 * C wrapper layer providing additional functionality and error handling
 * for the Python C API integration.
 */

#include "qxr_bridge.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Context implementation
struct QXRBridgeContext {
    QXRBridge* bridge;
    char* error_message;
    int last_error_code;
};

QXRBridgeContext* qxr_bridge_create_context(void) {
    QXRBridgeContext* ctx = malloc(sizeof(QXRBridgeContext));
    if (!ctx) return NULL;
    
    ctx->bridge = qxr_bridge_create();
    ctx->error_message = NULL;
    ctx->last_error_code = 0;
    
    if (!ctx->bridge) {
        qxr_bridge_set_error(ctx, -1, "Failed to create Rust bridge");
        return ctx;
    }
    
    return ctx;
}

void qxr_bridge_destroy_context(QXRBridgeContext* ctx) {
    if (!ctx) return;
    
    if (ctx->bridge) {
        qxr_bridge_destroy(ctx->bridge);
    }
    
    if (ctx->error_message) {
        free(ctx->error_message);
    }
    
    free(ctx);
}

int qxr_bridge_set_error(QXRBridgeContext* ctx, int code, const char* message) {
    if (!ctx) return -1;
    
    ctx->last_error_code = code;
    
    if (ctx->error_message) {
        free(ctx->error_message);
        ctx->error_message = NULL;
    }
    
    if (message) {
        size_t len = strlen(message) + 1;
        ctx->error_message = malloc(len);
        if (ctx->error_message) {
            strncpy(ctx->error_message, message, len);
        }
    }
    
    return code;
}

const char* qxr_bridge_get_error(QXRBridgeContext* ctx) {
    if (!ctx) return "Invalid context";
    return ctx->error_message ? ctx->error_message : "No error";
}

// Helper functions for Python integration
QXRResearchData* qxr_bridge_create_research_data(void) {
    QXRResearchData* data = malloc(sizeof(QXRResearchData));
    if (!data) return NULL;
    
    memset(data, 0, sizeof(QXRResearchData));
    return data;
}

void qxr_bridge_free_research_data(QXRResearchData* data) {
    if (!data) return;
    
    if (data->strategy_ptr) {
        free(data->strategy_ptr);
    }
    if (data->timeframe_ptr) {
        free(data->timeframe_ptr);
    }
    
    free(data);
}

int qxr_bridge_set_research_string(QXRResearchData* data, const char* str, int field) {
    if (!data || !str) return -1;
    
    size_t len = strlen(str);
    char* new_str = malloc(len + 1);
    if (!new_str) return -1;
    
    strcpy(new_str, str);
    
    switch (field) {
        case 0: // strategy
            if (data->strategy_ptr) free(data->strategy_ptr);
            data->strategy_ptr = new_str;
            data->strategy_len = len;
            break;
        case 1: // timeframe
            if (data->timeframe_ptr) free(data->timeframe_ptr);
            data->timeframe_ptr = new_str;
            data->timeframe_len = len;
            break;
        default:
            free(new_str);
            return -1;
    }
    
    return 0;
}

// Batch processing helper with error checking
int qxr_bridge_safe_batch_process(
    QXRBridgeContext* ctx,
    const QXRResearchData* data_array,
    size_t data_count,
    double* results
) {
    if (!ctx || !ctx->bridge) {
        return qxr_bridge_set_error(ctx, -1, "Invalid context or bridge");
    }
    
    if (!data_array || !results || data_count == 0) {
        return qxr_bridge_set_error(ctx, -2, "Invalid parameters");
    }
    
    int result = qxr_bridge_batch_process(ctx->bridge, data_array, data_count, results);
    if (result < 0) {
        qxr_bridge_set_error(ctx, result, "Batch processing failed");
    }
    
    return result;
}

// Safe content generation with bounds checking
int qxr_bridge_safe_generate_content(
    QXRBridgeContext* ctx,
    const QXRResearchData* data,
    const char* platform,
    char* output_buffer,
    size_t buffer_size
) {
    if (!ctx || !ctx->bridge) {
        return qxr_bridge_set_error(ctx, -1, "Invalid context or bridge");
    }
    
    if (!data || !platform || !output_buffer || buffer_size == 0) {
        return qxr_bridge_set_error(ctx, -2, "Invalid parameters");
    }
    
    int result = qxr_bridge_generate_content(
        ctx->bridge, data, platform, output_buffer, buffer_size
    );
    
    if (result < 0) {
        if (result == -2) {
            qxr_bridge_set_error(ctx, result, "Output buffer too small");
        } else {
            qxr_bridge_set_error(ctx, result, "Content generation failed");
        }
    }
    
    return result;
}

// Memory diagnostics for debugging
typedef struct {
    size_t total_allocated;
    size_t peak_allocated;
    size_t allocation_count;
    size_t deallocation_count;
} QXRMemoryStats;

static QXRMemoryStats memory_stats = {0, 0, 0, 0};

void* qxr_bridge_tracked_malloc(size_t size) {
    void* ptr = malloc(size);
    if (ptr) {
        memory_stats.total_allocated += size;
        memory_stats.allocation_count++;
        if (memory_stats.total_allocated > memory_stats.peak_allocated) {
            memory_stats.peak_allocated = memory_stats.total_allocated;
        }
    }
    return ptr;
}

void qxr_bridge_tracked_free(void* ptr, size_t size) {
    if (ptr) {
        free(ptr);
        memory_stats.total_allocated -= size;
        memory_stats.deallocation_count++;
    }
}

const QXRMemoryStats* qxr_bridge_get_memory_stats(void) {
    return &memory_stats;
}

void qxr_bridge_reset_memory_stats(void) {
    memset(&memory_stats, 0, sizeof(QXRMemoryStats));
}