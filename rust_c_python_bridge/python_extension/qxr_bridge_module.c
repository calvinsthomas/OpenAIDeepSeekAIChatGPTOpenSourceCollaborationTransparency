/**
 * QXR Bridge Python Extension Module
 * 
 * Python C API extension providing direct access to the Rust-C bridge
 * for high-performance QXR social media integration.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include "../c_bindings/qxr_bridge.h"

// Python object wrapping the bridge context
typedef struct {
    PyObject_HEAD
    QXRBridgeContext* ctx;
} QXRBridgeObject;

// QXRResearchData Python object
typedef struct {
    PyObject_HEAD
    QXRResearchData* data;
} QXRResearchDataObject;

// Forward declarations
static PyTypeObject QXRBridgeType;
static PyTypeObject QXRResearchDataType;

// QXRBridge methods
static void QXRBridge_dealloc(QXRBridgeObject* self) {
    if (self->ctx) {
        qxr_bridge_destroy_context(self->ctx);
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* QXRBridge_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    QXRBridgeObject* self;
    self = (QXRBridgeObject*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->ctx = qxr_bridge_create_context();
        if (!self->ctx) {
            Py_DECREF(self);
            PyErr_SetString(PyExc_RuntimeError, "Failed to create bridge context");
            return NULL;
        }
    }
    return (PyObject*)self;
}

static int QXRBridge_init(QXRBridgeObject* self, PyObject* args, PyObject* kwds) {
    return 0;
}

// Process research data method
static PyObject* QXRBridge_process_data(QXRBridgeObject* self, PyObject* args) {
    QXRResearchDataObject* data_obj;
    
    if (!PyArg_ParseTuple(args, "O!", &QXRResearchDataType, &data_obj)) {
        return NULL;
    }
    
    if (!self->ctx || !self->ctx->bridge || !data_obj->data) {
        PyErr_SetString(PyExc_RuntimeError, "Invalid bridge or data");
        return NULL;
    }
    
    double result = qxr_bridge_process_data(self->ctx->bridge, data_obj->data);
    if (result < 0) {
        PyErr_SetString(PyExc_RuntimeError, qxr_bridge_get_error(self->ctx));
        return NULL;
    }
    
    return PyFloat_FromDouble(result);
}

// Generate social media content method
static PyObject* QXRBridge_generate_content(QXRBridgeObject* self, PyObject* args) {
    QXRResearchDataObject* data_obj;
    const char* platform;
    
    if (!PyArg_ParseTuple(args, "O!s", &QXRResearchDataType, &data_obj, &platform)) {
        return NULL;
    }
    
    if (!self->ctx || !self->ctx->bridge || !data_obj->data) {
        PyErr_SetString(PyExc_RuntimeError, "Invalid bridge or data");
        return NULL;
    }
    
    char buffer[4096];
    int result = qxr_bridge_safe_generate_content(
        self->ctx, data_obj->data, platform, buffer, sizeof(buffer)
    );
    
    if (result < 0) {
        PyErr_SetString(PyExc_RuntimeError, qxr_bridge_get_error(self->ctx));
        return NULL;
    }
    
    return PyUnicode_FromString(buffer);
}

// Batch processing method
static PyObject* QXRBridge_batch_process(QXRBridgeObject* self, PyObject* args) {
    PyObject* data_list;
    
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &data_list)) {
        return NULL;
    }
    
    Py_ssize_t count = PyList_Size(data_list);
    if (count <= 0) {
        PyErr_SetString(PyExc_ValueError, "Empty data list");
        return NULL;
    }
    
    // Allocate arrays for C processing
    QXRResearchData* data_array = malloc(count * sizeof(QXRResearchData));
    double* results = malloc(count * sizeof(double));
    
    if (!data_array || !results) {
        free(data_array);
        free(results);
        return PyErr_NoMemory();
    }
    
    // Extract data from Python list
    for (Py_ssize_t i = 0; i < count; i++) {
        PyObject* item = PyList_GetItem(data_list, i);
        if (!PyObject_IsInstance(item, (PyObject*)&QXRResearchDataType)) {
            free(data_array);
            free(results);
            PyErr_SetString(PyExc_TypeError, "List must contain QXRResearchData objects");
            return NULL;
        }
        
        QXRResearchDataObject* data_obj = (QXRResearchDataObject*)item;
        data_array[i] = *(data_obj->data);
    }
    
    // Process batch
    int result = qxr_bridge_safe_batch_process(self->ctx, data_array, count, results);
    if (result < 0) {
        free(data_array);
        free(results);
        PyErr_SetString(PyExc_RuntimeError, qxr_bridge_get_error(self->ctx));
        return NULL;
    }
    
    // Create Python list of results
    PyObject* py_results = PyList_New(count);
    for (Py_ssize_t i = 0; i < count; i++) {
        PyList_SetItem(py_results, i, PyFloat_FromDouble(results[i]));
    }
    
    free(data_array);
    free(results);
    
    return py_results;
}

// Get bridge version
static PyObject* QXRBridge_version(QXRBridgeObject* self, PyObject* Py_UNUSED(ignored)) {
    return PyUnicode_FromString(qxr_bridge_version());
}

// QXRBridge method definitions
static PyMethodDef QXRBridge_methods[] = {
    {"process_data", (PyCFunction)QXRBridge_process_data, METH_VARARGS,
     "Process research data and return performance score"},
    {"generate_content", (PyCFunction)QXRBridge_generate_content, METH_VARARGS,
     "Generate social media content for a platform"},
    {"batch_process", (PyCFunction)QXRBridge_batch_process, METH_VARARGS,
     "Process multiple research data items in batch"},
    {"version", (PyCFunction)QXRBridge_version, METH_NOARGS,
     "Get bridge version information"},
    {NULL}
};

// QXRBridge type definition
static PyTypeObject QXRBridgeType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "qxr_bridge.QXRBridge",
    .tp_basicsize = sizeof(QXRBridgeObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor)QXRBridge_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "QXR Bridge for high-performance Rust-C-Python integration",
    .tp_methods = QXRBridge_methods,
    .tp_init = (initproc)QXRBridge_init,
    .tp_new = QXRBridge_new,
};

// QXRResearchData methods
static void QXRResearchData_dealloc(QXRResearchDataObject* self) {
    if (self->data) {
        qxr_bridge_free_research_data(self->data);
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* QXRResearchData_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    QXRResearchDataObject* self;
    self = (QXRResearchDataObject*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->data = qxr_bridge_create_research_data();
        if (!self->data) {
            Py_DECREF(self);
            return PyErr_NoMemory();
        }
    }
    return (PyObject*)self;
}

static int QXRResearchData_init(QXRResearchDataObject* self, PyObject* args, PyObject* kwds) {
    static char* kwlist[] = {
        "signals", "opportunities", "signal_strength", 
        "price_range_min", "price_range_max", "max_liquidity",
        "strategy", "timeframe", NULL
    };
    
    int signals = 0, opportunities = 0;
    double signal_strength = 0.0, price_range_min = 0.0, price_range_max = 0.0;
    long long max_liquidity = 0;
    const char* strategy = "";
    const char* timeframe = "";
    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iidddLss", kwlist,
                                     &signals, &opportunities, &signal_strength,
                                     &price_range_min, &price_range_max, &max_liquidity,
                                     &strategy, &timeframe)) {
        return -1;
    }
    
    if (!self->data) {
        PyErr_SetString(PyExc_RuntimeError, "Data not initialized");
        return -1;
    }
    
    self->data->signals = signals;
    self->data->opportunities = opportunities;
    self->data->signal_strength = signal_strength;
    self->data->price_range_min = price_range_min;
    self->data->price_range_max = price_range_max;
    self->data->max_liquidity = max_liquidity;
    
    if (qxr_bridge_set_research_string(self->data, strategy, 0) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to set strategy");
        return -1;
    }
    
    if (qxr_bridge_set_research_string(self->data, timeframe, 1) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to set timeframe");
        return -1;
    }
    
    return 0;
}

// QXRResearchData property getters/setters
static PyObject* QXRResearchData_get_signals(QXRResearchDataObject* self, void* closure) {
    return PyLong_FromLong(self->data->signals);
}

static int QXRResearchData_set_signals(QXRResearchDataObject* self, PyObject* value, void* closure) {
    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "signals must be an integer");
        return -1;
    }
    self->data->signals = PyLong_AsLong(value);
    return 0;
}

// Property definitions
static PyGetSetDef QXRResearchData_getsetters[] = {
    {"signals", (getter)QXRResearchData_get_signals, (setter)QXRResearchData_set_signals,
     "Number of trading signals", NULL},
    {NULL}
};

// QXRResearchData type definition
static PyTypeObject QXRResearchDataType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "qxr_bridge.QXRResearchData",
    .tp_basicsize = sizeof(QXRResearchDataObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor)QXRResearchData_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "QXR Research Data container",
    .tp_init = (initproc)QXRResearchData_init,
    .tp_new = QXRResearchData_new,
    .tp_getset = QXRResearchData_getsetters,
};

// Module methods
static PyObject* qxr_bridge_get_memory_stats(PyObject* self, PyObject* args) {
    const QXRMemoryStats* stats = qxr_bridge_get_memory_stats();
    return Py_BuildValue("{s:K,s:K,s:K,s:K}",
                        "total_allocated", (unsigned long long)stats->total_allocated,
                        "peak_allocated", (unsigned long long)stats->peak_allocated,
                        "allocation_count", (unsigned long long)stats->allocation_count,
                        "deallocation_count", (unsigned long long)stats->deallocation_count);
}

// Module method definitions
static PyMethodDef qxr_bridge_methods[] = {
    {"get_memory_stats", qxr_bridge_get_memory_stats, METH_NOARGS,
     "Get memory allocation statistics"},
    {NULL}
};

// Module definition
static struct PyModuleDef qxr_bridge_module = {
    PyModuleDef_HEAD_INIT,
    "qxr_bridge",
    "High-performance Rust-C-Python bridge for QXR system",
    -1,
    qxr_bridge_methods
};

// Module initialization
PyMODINIT_FUNC PyInit_qxr_bridge(void) {
    PyObject* m;
    
    if (PyType_Ready(&QXRBridgeType) < 0)
        return NULL;
    
    if (PyType_Ready(&QXRResearchDataType) < 0)
        return NULL;
    
    m = PyModule_Create(&qxr_bridge_module);
    if (m == NULL)
        return NULL;
    
    Py_INCREF(&QXRBridgeType);
    if (PyModule_AddObject(m, "QXRBridge", (PyObject*)&QXRBridgeType) < 0) {
        Py_DECREF(&QXRBridgeType);
        Py_DECREF(m);
        return NULL;
    }
    
    Py_INCREF(&QXRResearchDataType);
    if (PyModule_AddObject(m, "QXRResearchData", (PyObject*)&QXRResearchDataType) < 0) {
        Py_DECREF(&QXRResearchDataType);
        Py_DECREF(m);
        return NULL;
    }
    
    return m;
}