/*!
 * QXR Rust-C-Python Bridge
 * 
 * A high-performance bridge providing direct memory access between Rust, C, and Python
 * for the QXR social media integration system. This eliminates the need for serialization
 * (pickling) or file-based communication.
 */

use std::ffi::CStr;
use std::os::raw::{c_char, c_int, c_double, c_void};
use std::slice;

/// Research data structure for QXR system
#[derive(Debug, Clone)]
#[repr(C)]
pub struct QXRResearchData {
    pub signals: i32,
    pub opportunities: i32,
    pub signal_strength: f64,
    pub price_range_min: f64,
    pub price_range_max: f64,
    pub max_liquidity: i64,
    pub strategy_len: usize,
    pub strategy_ptr: *mut c_char,
    pub timeframe_len: usize,
    pub timeframe_ptr: *mut c_char,
}

/// Social media post structure
#[derive(Debug, Clone)]
#[repr(C)]
pub struct QXRSocialPost {
    pub platform_len: usize,
    pub platform_ptr: *mut c_char,
    pub content_len: usize,
    pub content_ptr: *mut c_char,
    pub hashtags_count: usize,
    pub hashtags_ptr: *mut *mut c_char,
    pub engagement_score: f64,
}

/// Bridge context for managing memory and state
pub struct QXRBridge {
    pub research_data: Option<QXRResearchData>,
    pub social_posts: Vec<QXRSocialPost>,
    pub memory_allocations: Vec<*mut c_void>,
}

impl QXRBridge {
    pub fn new() -> Self {
        QXRBridge {
            research_data: None,
            social_posts: Vec::new(),
            memory_allocations: Vec::new(),
        }
    }

    /// Process research data with high-performance calculations
    pub fn process_research_data(&mut self, data: &QXRResearchData) -> f64 {
        // High-performance signal processing
        let base_score = data.signals as f64 * data.signal_strength;
        let liquidity_factor = (data.max_liquidity as f64).ln() / 10.0;
        let opportunity_multiplier = 1.0 + (data.opportunities as f64 / 100.0);
        
        base_score * liquidity_factor * opportunity_multiplier
    }

    /// Generate optimized social media content
    pub fn generate_social_content(&mut self, research_data: &QXRResearchData, platform: &str) -> String {
        let performance_score = self.process_research_data(research_data);
        
        match platform {
            "linkedin" => format!(
                "🚀 QXR Research Update: {} signals detected with {:.3} strength. \
                Performance score: {:.2}. {} opportunities identified in {}.",
                research_data.signals,
                research_data.signal_strength,
                performance_score,
                research_data.opportunities,
                unsafe { CStr::from_ptr(research_data.timeframe_ptr).to_str().unwrap_or("24h") }
            ),
            "twitter" => format!(
                "🔥 {} signals @ {:.3} strength | Score: {:.1} | {} ops | {} #QXR #Trading",
                research_data.signals,
                research_data.signal_strength,
                performance_score,
                research_data.opportunities,
                unsafe { CStr::from_ptr(research_data.timeframe_ptr).to_str().unwrap_or("24h") }
            ),
            _ => format!("QXR Analysis: {} signals, performance {:.2}", research_data.signals, performance_score)
        }
    }
}

/// C FFI exports for the bridge
#[no_mangle]
pub extern "C" fn qxr_bridge_create() -> *mut QXRBridge {
    let bridge = Box::new(QXRBridge::new());
    Box::into_raw(bridge)
}

#[no_mangle]
pub extern "C" fn qxr_bridge_destroy(bridge: *mut QXRBridge) {
    if !bridge.is_null() {
        unsafe {
            let bridge = Box::from_raw(bridge);
            // Memory cleanup happens automatically with Box drop
            drop(bridge);
        }
    }
}

#[no_mangle]
pub extern "C" fn qxr_bridge_process_data(
    bridge: *mut QXRBridge,
    data: *const QXRResearchData
) -> c_double {
    if bridge.is_null() || data.is_null() {
        return -1.0;
    }
    
    unsafe {
        let bridge_ref = &mut *bridge;
        let data_ref = &*data;
        bridge_ref.process_research_data(data_ref)
    }
}

#[no_mangle]
pub extern "C" fn qxr_bridge_generate_content(
    bridge: *mut QXRBridge,
    data: *const QXRResearchData,
    platform: *const c_char,
    output_buffer: *mut c_char,
    buffer_size: usize
) -> c_int {
    if bridge.is_null() || data.is_null() || platform.is_null() || output_buffer.is_null() {
        return -1;
    }
    
    unsafe {
        let bridge_ref = &mut *bridge;
        let data_ref = &*data;
        let platform_str = CStr::from_ptr(platform).to_str().unwrap_or("default");
        
        let content = bridge_ref.generate_social_content(data_ref, platform_str);
        let content_bytes = content.as_bytes();
        
        if content_bytes.len() >= buffer_size {
            return -2; // Buffer too small
        }
        
        std::ptr::copy_nonoverlapping(
            content_bytes.as_ptr(),
            output_buffer as *mut u8,
            content_bytes.len()
        );
        
        // Null terminate
        *(output_buffer.add(content_bytes.len())) = 0;
        
        content_bytes.len() as c_int
    }
}

/// Batch processing for multiple datasets
#[no_mangle]
pub extern "C" fn qxr_bridge_batch_process(
    bridge: *mut QXRBridge,
    data_array: *const QXRResearchData,
    data_count: usize,
    results: *mut c_double
) -> c_int {
    if bridge.is_null() || data_array.is_null() || results.is_null() {
        return -1;
    }
    
    unsafe {
        let bridge_ref = &mut *bridge;
        let data_slice = slice::from_raw_parts(data_array, data_count);
        let results_slice = slice::from_raw_parts_mut(results, data_count);
        
        for (i, data) in data_slice.iter().enumerate() {
            results_slice[i] = bridge_ref.process_research_data(data);
        }
        
        data_count as c_int
    }
}

/// Memory allocation helper for Python integration
#[no_mangle]
pub extern "C" fn qxr_bridge_alloc_string(len: usize) -> *mut c_char {
    let layout = std::alloc::Layout::array::<u8>(len + 1).unwrap();
    unsafe {
        let ptr = std::alloc::alloc(layout) as *mut c_char;
        if !ptr.is_null() {
            *ptr.add(len) = 0; // Null terminate
        }
        ptr
    }
}

#[no_mangle]
pub extern "C" fn qxr_bridge_free_string(ptr: *mut c_char) {
    if !ptr.is_null() {
        unsafe {
            let layout = std::alloc::Layout::array::<u8>(1).unwrap();
            std::alloc::dealloc(ptr as *mut u8, layout);
        }
    }
}

/// Get bridge version info
#[no_mangle]
pub extern "C" fn qxr_bridge_version() -> *const c_char {
    "QXR Bridge v0.1.0\0".as_ptr() as *const c_char
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::ffi::CString;

    #[test]
    fn test_bridge_creation() {
        let bridge = QXRBridge::new();
        assert!(bridge.research_data.is_none());
        assert_eq!(bridge.social_posts.len(), 0);
    }

    #[test]
    fn test_research_data_processing() {
        let mut bridge = QXRBridge::new();
        
        let strategy = CString::new("ETH Statistical Arbitrage").unwrap();
        let timeframe = CString::new("24h").unwrap();
        
        let data = QXRResearchData {
            signals: 45,
            opportunities: 8,
            signal_strength: 1.247,
            price_range_min: 3420.0,
            price_range_max: 3580.0,
            max_liquidity: 12500000,
            strategy_len: strategy.as_bytes().len(),
            strategy_ptr: strategy.as_ptr() as *mut c_char,
            timeframe_len: timeframe.as_bytes().len(),
            timeframe_ptr: timeframe.as_ptr() as *mut c_char,
        };
        
        let score = bridge.process_research_data(&data);
        assert!(score > 0.0);
    }

    #[test]
    fn test_social_content_generation() {
        let mut bridge = QXRBridge::new();
        
        let strategy = CString::new("ETH Statistical Arbitrage").unwrap();
        let timeframe = CString::new("24h").unwrap();
        
        let data = QXRResearchData {
            signals: 45,
            opportunities: 8,
            signal_strength: 1.247,
            price_range_min: 3420.0,
            price_range_max: 3580.0,
            max_liquidity: 12500000,
            strategy_len: strategy.as_bytes().len(),
            strategy_ptr: strategy.as_ptr() as *mut c_char,
            timeframe_len: timeframe.as_bytes().len(),
            timeframe_ptr: timeframe.as_ptr() as *mut c_char,
        };
        
        let content = bridge.generate_social_content(&data, "linkedin");
        assert!(content.contains("45 signals"));
        assert!(content.contains("1.247"));
        
        let twitter_content = bridge.generate_social_content(&data, "twitter");
        assert!(twitter_content.len() <= 280); // Twitter character limit
    }
}