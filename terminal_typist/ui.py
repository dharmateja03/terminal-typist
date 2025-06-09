# Legacy import redirect for backwards compatibility
# The UI has been restructured into modular components

from .ui import GameUI

# Re-export for backwards compatibility
__all__ = ['GameUI']