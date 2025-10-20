import tempfile as _tf, shutil as _shutil
_orig = _tf.TemporaryDirectory.cleanup
def _safe(self):
    try:
        _orig(self)
    except Exception:
        try: _shutil.rmtree(self.name, ignore_errors=True)
        except Exception: pass
_tf.TemporaryDirectory.cleanup = _safe

try:
    _orig_rm = _shutil._rmtree_safe_fd
    def _safe_rm(stack, onexc):
        try: return _orig_rm(stack, onexc)
        except TypeError: return
    _shutil._rmtree_safe_fd = _safe_rm
except Exception:
    pass
