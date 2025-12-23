from __future__ import annotations
from pathlib import Path
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageOps
from collections.abc import Callable
from typing import Any
import time
import re
import random
import threading
import html
import sys
import os
import platform
import ctypes
from ctypes import wintypes
from library_data import LibraryData


def resource_path(*parts: str) -> Path:
    """
    Return an absolute Path to a bundled resource (PyInstaller) or dev file.
    Usage: resource_path("ASSETS", "main menu.png")
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)  # PyInstaller temp dir
    else:
        base = Path(__file__).resolve().parent
    return base.joinpath(*parts)

ASSETS_DIR = resource_path("ASSETS")

# ============================================================================
#                          PATHS & FILE LOCATIONS
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent         # dev convenience


# --- Theme Background Images ---
BG_IMAGE_PATH          = ASSETS_DIR / "main menu.png"
BROWSE_GENRES_BG_IMG   = ASSETS_DIR / "browse genres.png"
SHOW_BOOKS_BG_IMG      = ASSETS_DIR / "show books.png"
BOOK_INFO_BG_IMG       = ASSETS_DIR / "book info.png"
MENU_BTN_IMG           = ASSETS_DIR / "menu button.png"
SIDE_MENU_BG_IMG       = ASSETS_DIR / "side_menu.png"
SETTINGS_BG_IMG        = ASSETS_DIR / "settings.png"
COLLECTIONS_BG_IMG     = ASSETS_DIR / "collections.png"
OPEN_COLLECTION_BG_IMG = ASSETS_DIR / "open collection.png"

# ============================================================================
#                           SET THEME COLORS
#       (5-10 base theme colors - all visual theming derives from these)
# ============================================================================
THEME_COLOR00   = "#000000"   # Black
THEME_COLOR1    = "#003B32"   # Primary dark green
THEME_COLOR2    = "#FFFFFF"   # White / light background
THEME_COLOR3    = "#F4E6D3"   # Warm cream / highlight
THEME_COLOR4    = "#E0D9D7"   # Soft gray / secondary surface
THEME_COLOR5    = "#111111"   # Near black / primary text
THEME_COLOR6    = "#666666"   # Medium gray / muted text
THEME_COLOR7    = "#DDDDDD"   # Light gray / borders
THEME_COLOR8    = "#DBD5D5"   # Warm light gray / grid backgrounds
THEME_COLOR9    = "#585858"
THEME_COLOR10   = "#EFEFEF"
THEME_COLOR11   = "#333333"
THEME_COLOR12   = "#FFEBEE" # RED

# ============================================================================
#                    SHARED THEME CONSTANTS
#      (Variables controlling appearance across multiple pages/cards)
#      Organized by: 1. Colors  2. Sizes  3. Unique Traits
# ============================================================================

# ------------------ 1. COLORS ------------------

# "FLOATING" TEXT
BACKGROUND_TITLE_TEXT             = THEME_COLOR2

# TABLE HEADER COLORS
SHARED_MAINHEADER_BG_COLOR           = THEME_COLOR1
SHARED_MAINHEADER_SUBTEXT_COLOR      = THEME_COLOR3
SHARED_SUBHEADER_BG_COLOR            = THEME_COLOR3
SHARED_SUBHEADER_TEXT_COLOR          = THEME_COLOR1
# TABLE
SHARED_MAINHEADER2_BG_COLOR         = THEME_COLOR2
SHARED_MAINHEADER2_TEXT_COLOR       = THEME_COLOR1

# Panels / Surfaces / Borders (shared UI building blocks)
FOCUS_PANEL_BG_COLOR              = THEME_COLOR2
FOCUS_PANEL_TEXT_COLOR                 = THEME_COLOR5
FOCUS_PANEL_MUTED_TEXT_COLOR              = THEME_COLOR6
FOCUS_PANEL_ACCENT_COLOR                  = THEME_COLOR7
SHARED_PANEL_BG_COLOR                = THEME_COLOR4
SORT_VIEW_BG                      =  THEME_COLOR2

# Scroll Windows / Tables / Lists (shared)
SHARED_SCROLL_BG_COLOR               = THEME_COLOR2
SHARED_TABLE_BG_COLOR                = THEME_COLOR2
SHARED_TABLE_ALTROW_BG_COLOR         = THEME_COLOR4
SHARED_SCROLLROW_TEXT_COLOR          = THEME_COLOR5
SHARED_EMPTYTABLE_BG_COLOR           = THEME_COLOR2
SHARED_EMPTYTABLE_TEXT_COLOR         = THEME_COLOR1

SHARED_SCROLLROW2_TEXT_COLOR         = THEME_COLOR2
SHARED_TABLE2_BG_COLOR               = THEME_COLOR11
SHARED_TABLE2_ALTROW_BG_COLOR        = THEME_COLOR6

# Mini Labels (shared)
SHARED_MINILABEL_BG_COLOR            = THEME_COLOR1
SHARED_MINILABEL_TEXT_COLOR          = THEME_COLOR4

# Primary Button (neutral)
SHARED_BUTTON1_BG_COLOR              = THEME_COLOR3
SHARED_BUTTON1_TEXT_COLOR            = THEME_COLOR1
SHARED_BUTTON1_BG_ONCLICK_COLOR      = THEME_COLOR10
SHARED_BUTTON1_TEXT_ONCLICK_COLOR    = THEME_COLOR1

# Accent Main Button
SHARED_BUTTON2_BG_COLOR              = THEME_COLOR1
SHARED_BUTTON2_TEXT_COLOR            = THEME_COLOR4
SHARED_BUTTON2_BG_ONCLICK_COLOR      = THEME_COLOR10
SHARED_BUTTON2_TEXT_ONCLICK_COLOR    = THEME_COLOR9

# Side Menu Buttons
SHARED_SIDEMENU_BTN_BG_COLOR         = THEME_COLOR3
SHARED_SIDEMENU_BTN_TEXT_COLOR       = THEME_COLOR5
SHARED_SIDEMENU_BTN_BG_ONCLICK_COLOR = THEME_COLOR10
SHARED_SIDEMENU_BTN_TEXT_ONCLICK_COLOR = THEME_COLOR11

# Search Bar Button (icon/button near entry)
SHARED_SEARCHBTN_BG_COLOR            = THEME_COLOR1
SHARED_SEARCHBTN_BG_ONCLICK_COLOR    = THEME_COLOR5

# X (Remove) and + (Add) Buttons
SHARED_XBTN_SELECTED_BG_COLOR        = THEME_COLOR12
SHARED_XBTN_SELECTED_ONCLICK_COLOR   = THEME_COLOR12
SHARED_XBTN_BG_COLOR                 = THEME_COLOR9
SHARED_XBTN_BG_ONCLICK_COLOR         = THEME_COLOR11
SHARED_XBTN_IDLE_COLOR               = THEME_COLOR5

SHARED_PLUSICON_IDLE_COLOR           = THEME_COLOR2
SHARED_PLUSICON_CLICKED_COLOR        = THEME_COLOR9
SHARED_PLUSBTN_BG_COLOR              = THEME_COLOR9

# Missing-Info Tiles
SHARED_BLANKCOVER_BG_COLOR           = THEME_COLOR2
SHARED_BLANKCOVER_TEXT_COLOR         = THEME_COLOR9
SHARED_BLANKCOLLECTION_TILEBG_COLOR      = THEME_COLOR9
SHARED_BLANKCOLLECTION_TILEACCENT_COLOR = THEME_COLOR2

# Radio Buttons
SHARED_RADIO_BG_COLOR                = THEME_COLOR1
SHARED_RADIO_TEXT_COLOR              = THEME_COLOR2
SHARED_RADIO_HIGHLIGHT_COLOR         = THEME_COLOR2

# Alphabet Jump-To Bar
SHARED_ALPHABAR_BG_COLOR             = THEME_COLOR1
ALPHABAR_BORDER_COLOR                = THEME_COLOR1
SHARED_ALPHA_CLICKABLE_BG_COLOR      = THEME_COLOR1
SHARED_ALPHA_CLICKABLE_TEXT_COLOR    = THEME_COLOR2
SHARED_ALPHA_HOVER_BG_COLOR          = THEME_COLOR2
SHARED_ALPHA_HOVER_TEXT_COLOR        = THEME_COLOR5
SHARED_ALPHA_MUTED_BG_COLOR          = THEME_COLOR11
SHARED_ALPHA_MUTED_TEXT_COLOR        = THEME_COLOR10
SHARED_ALPHA_SELECTED_BG_COLOR       = THEME_COLOR10
SHARED_ALPHA_SELECTED_TEXT_COLOR     = THEME_COLOR5

# Entry / Input Fields
SHARED_ENTRY1_BORDER_COLOR           = THEME_COLOR9
SHARED_ENTRY1_BG_COLOR               = THEME_COLOR2
SHARED_ENTRY1_TEXT_COLOR             = THEME_COLOR5
SHARED_ENTRY_CURSOR_COLOR            = THEME_COLOR1

SHARED_ENTRY2_BORDER_COLOR           = THEME_COLOR9
SHARED_ENTRY2_BG_COLOR               = THEME_COLOR2
SHARED_ENTRY2_TEXT_COLOR             = THEME_COLOR5
SHARED_ENTRY2_CURSOR_COLOR           = THEME_COLOR1


# ------------------ 2. SIZES ------------------

# Global Window Dimensions
SHARED_WINDOW_DESIGN_WIDTH           = 1280
SHARED_WINDOW_DESIGN_HEIGHT          = 920

# Navigation Stack
SHARED_NAV_STACK_XPOS                = 60
SHARED_NAV_STACK_BOTTOM_YPOS         = SHARED_WINDOW_DESIGN_HEIGHT - 35
SHARED_NAV_BTN_WIDTH                 = 220
SHARED_NAV_BTN_HEIGHT                = 44
SHARED_NAV_GAP_Y                     = 10

# General Buttons
SHARED_BUTTON_BORDER_WIDTH           = 0
SHARED_BUTTON_DEFAULT_WIDTH          = 350
SHARED_BUTTON_DEFAULT_HEIGHT         = 50

# Entry Bar
SHARED_ENTRY_FRAME_BORDER_WIDTH      = 0
SHARED_ENTRY_FRAME_HIGHLIGHT_WIDTH   = 0
SHARED_ENTRY_BORDER_PX               = 3
SHARED_ENTRY_FONT_SIZE               = 16

# Scroll Container Defaults
SHARED_SCROLL_RELX                   = 0.5
SHARED_SCROLL_RELY                   = 0.5
SHARED_SCROLL_RELWIDTH               = 0.88
SHARED_SCROLL_RELHEIGHT              = 0.68
SHARED_SCROLLBAR_WIDTH               = 14

# Alphabet Bar
SHARED_ALPHABAR_HEIGHT               = 36

# X Button (Remove)
SHARED_XBTN_SIZE                     = 18

# Plus Button (Add)
SHARED_PLUSBTN_SIZE                  = 34

# ------------------ 3. UNIQUE TRAITS ------------------

# Entry Bar Traits
SHARED_ENTRY_RELIEF_STYLE            = "flat"
SHARED_ENTRY_JUSTIFY_STYLE           = "right"

# Font Families
SHARED_FONT_CUSTOM                   = "AESTHICA"
SHARED_FONT_BUTTON                   = "Sherly Kitchen"
SHARED_FONT_TABLE                    = "liberation-sans"
ENTRY_BAR_FONT_FAMILY                = "AESTHICA"

# Font Tuples
SHARED_TABLE_HEADER_FONT             = ("liberation-sans", 20, "bold")
SHARED_TABLE_ROW_FONT                = ("liberation-sans", 18)

# Window
SHARED_WINDOW_TITLE                  = "Library Manager"


# ============================================================================
#                       PAGE SPECIFIC CONSTANTS
#      (Grouped by page - each section has: 1. Colors  2. Sizes  3. Traits)
# ============================================================================

# ----------------------------------------------------------------------------
# MAIN MENU PAGE
# ----------------------------------------------------------------------------
# 1. Colors
MAINMENU_LABEL_FG_COLOR              = THEME_COLOR5

# 2. Sizes
MAINMENU_TITLE_FONT_SIZE             = 82
MAINMENU_SUBTITLE_FONT_SIZE          = 28
MAINMENU_BUTTON_FONT_SIZE            = 28
MAINMENU_SMALL_BUTTON_FONT_SIZE      = 22


# ----------------------------------------------------------------------------
# SETTINGS PAGE
# ----------------------------------------------------------------------------
# 1. Colors
SETTINGS_LABEL_FG_COLOR              = THEME_COLOR5


# ----------------------------------------------------------------------------
# BOOK EDIT PAGE
# ----------------------------------------------------------------------------
# 1. Colors
BOOKEDIT_DESC_BG_COLOR               = THEME_COLOR10
BOOKEDIT_DESC_TEXT_COLOR             = THEME_COLOR5


# ----------------------------------------------------------------------------
# BROWSE GENRES PAGE
# ----------------------------------------------------------------------------
# 1. Colors - Genre Tile Buttons
BROWSEGENRES_TILE_BG_COLOR           = THEME_COLOR3
BROWSEGENRES_TILE_TEXT_COLOR         = THEME_COLOR5
BROWSEGENRES_TILE_BG_ONCLICK_COLOR   = THEME_COLOR6
BROWSEGENRES_TILE_TEXT_ONCLICK_COLOR = THEME_COLOR1

# 1. Colors - Layout/Panels
BROWSEGENRES_GRID_BG_COLOR           = THEME_COLOR8
BROWSEGENRES_PANEL_BG_COLOR          = THEME_COLOR4
BROWSEGENRES_LABEL_FG_COLOR          = THEME_COLOR5
BROWSEGENRES_EMPTY_FG_COLOR          = THEME_COLOR1

# 2. Sizes - Grid Panel
BROWSEGENRES_PANEL_RELX              = 0.5
BROWSEGENRES_PANEL_RELY              = 0.55
BROWSEGENRES_PANEL_RELWIDTH          = 0.86
BROWSEGENRES_PANEL_RELHEIGHT         = 0.50

# 2. Sizes - Genre Tile Buttons
BROWSEGENRES_TILE_HEIGHT_NORMAL      = 60
BROWSEGENRES_TILE_HEIGHT_FULLSCREEN  = 70
BROWSEGENRES_TILE_MIN_WIDTH_NORMAL   = 200
BROWSEGENRES_TILE_MIN_WIDTH_FULLSCREEN = 220
BROWSEGENRES_TILE_GAP_X              = 18
BROWSEGENRES_TILE_GAP_Y              = 18
BROWSEGENRES_TILE_MAX_COLS_NORMAL    = 3
BROWSEGENRES_TILE_MAX_COLS_FULLSCREEN = 5

# 2. Sizes - Category Dropdown
BROWSEGENRES_CATEGORY_XPOS           = 1070
BROWSEGENRES_CATEGORY_YPOS           = 220
BROWSEGENRES_CATEGORY_WIDTH          = 220
BROWSEGENRES_CATEGORY_HEIGHT         = 50
BROWSEGENRES_CATEGORY_FONT_SIZE      = 22
BROWSEGENRES_CATEGORY_COMBO_WIDTH    = 10
BROWSEGENRES_CATEGORY_COMBO_FONT_SIZE = 20

# 2. Sizes - Title
BROWSEGENRES_TITLE_RELY              = 0.2

# 3. Traits
BROWSEGENRES_EMPTYMSG_FONT_SIZE      = 26


# ----------------------------------------------------------------------------
# GENRE PAGE (Single Genre View)
# ----------------------------------------------------------------------------
# 1. Colors
GENREPAGE_ROW_FG_COLOR               = THEME_COLOR5

# 2. Sizes
GENREPAGE_TITLE_FONT_SIZE            = 34
GENREPAGE_ALPHABAR_RELY              = 0.17
GENREPAGE_SCROLL_RELWIDTH            = 0.88
GENREPAGE_SCROLL_RELHEIGHT           = 0.70
GENREPAGE_HEADER_HEIGHT              = 60
GENREPAGE_HEADER_PAD_X               = 18
GENREPAGE_HEADER_PAD_Y               = 10


# ----------------------------------------------------------------------------
# VIEW ALL PAGE
# ----------------------------------------------------------------------------
# 1. Colors
VIEWALL_ROW_FG_COLOR                 = THEME_COLOR5


# ----------------------------------------------------------------------------
# SEARCH RESULTS PAGE
# ----------------------------------------------------------------------------
# 1. Colors
SEARCHRESULTS_HEADER_BG_COLOR        = THEME_COLOR1
SEARCHRESULTS_CARD_BG_COLOR          = THEME_COLOR2
SEARCHRESULTS_ROW_FG_COLOR           = THEME_COLOR5
SEARCHRESULTS_HEADING_FG_COLOR       = THEME_COLOR1

# 2. Sizes
SEARCHRESULTS_SEARCHBAR_XPOS         = 540
SEARCHRESULTS_SEARCHBAR_YPOS         = 100
SEARCHRESULTS_SEARCHBAR_WIDTH        = 600
SEARCHRESULTS_SEARCHBAR_HEIGHT       = 35
SEARCHRESULTS_SEARCHBAR_FONT_SIZE    = 22
SEARCHRESULTS_TITLE_FONT_SIZE        = 34
SEARCHRESULTS_ALPHABAR_RELY          = 0.26
SEARCHRESULTS_SCROLL_RELWIDTH        = 0.88
SEARCHRESULTS_SCROLL_RELHEIGHT       = 0.60
SEARCHRESULTS_HEADER_HEIGHT          = 60
SEARCHRESULTS_HEADER_PAD_X           = 18
SEARCHRESULTS_HEADER_PAD_Y           = 10


# ----------------------------------------------------------------------------
# COLLECTIONS PAGE
# ----------------------------------------------------------------------------
# 1. Colors
COLLECTIONS_HEADER_BG_COLOR          = THEME_COLOR1
COLLECTIONS_HEADER_SUBTEXT_COLOR     = THEME_COLOR3
COLLECTIONS_LABEL_FG_COLOR           = THEME_COLOR5
COLLECTIONS_META_FG_COLOR            = THEME_COLOR5
COLLECTIONS_NAME_FG_COLOR            = THEME_COLOR5

# 2. Sizes
COLLECTIONS_TITLE_FONT_SIZE          = 28
COLLECTIONS_SUB_FONT_SIZE            = 14
COLLECTIONS_BTN_FONT_SIZE            = 16
COLLECTIONS_LIST_FONT_SIZE           = 16
COLLECTIONS_HEADER_PAD_X             = 20
COLLECTIONS_HEADER_PAD_Y_TOP         = 16
COLLECTIONS_HEADER_PAD_Y_BOTTOM      = 8
COLLECTIONS_BODY_PAD_X               = 20
COLLECTIONS_BODY_PAD_Y_TOP           = 8
COLLECTIONS_BODY_PAD_Y_BOTTOM        = 10
COLLECTIONS_FOOTER_PAD_X             = 20
COLLECTIONS_FOOTER_PAD_Y             = 16


# ----------------------------------------------------------------------------
# OPEN COLLECTION PAGE
# ----------------------------------------------------------------------------
# 1. Colors
OPENCOLL_HEADER_BG_COLOR             = THEME_COLOR4
OPENCOLL_HEADER_FG_COLOR             = THEME_COLOR2


# ----------------------------------------------------------------------------
# BUILD COLLECTION PAGE
# ----------------------------------------------------------------------------
# 1. Colors - Left Panel
BUILDCOLL_LEFTPAN_BG_COLOR           = THEME_COLOR4
BUILDCOLL_LEFTPAN_LIST_BG_COLOR      = THEME_COLOR2
BUILDCOLL_LEFTPAN_HEADER_TEXT_COLOR  = THEME_COLOR1
BUILDCOLL_LEFTPAN_LIST_TEXT_COLOR    = THEME_COLOR5

BUILDCOLL_PLUSBTN_BG_COLOR          = THEME_COLOR8
BUILDCOLL_PLUSBTN_CLICKABLE_COLOR   = THEME_COLOR1
BUILDCOLL_PLUSICON_ONCLICK_COLOR    = THEME_COLOR5


# 1. Colors - Right Panel
BUILDCOLL_RIGHTPAN_BG_COLOR          = THEME_COLOR1
BUILDCOLL_RIGHTPAN_LIST_BG_COLOR     = THEME_COLOR2
BUILDCOLL_RIGHTPAN_HEADER_TEXT_COLOR = THEME_COLOR4
BUILDCOLL_RIGHTPAN_SUB_TEXT_COLOR    = THEME_COLOR9
BUILDCOLL_RIGHTPAN_LIST_TEXT_COLOR   = THEME_COLOR5

# 2. Sizes
BUILDCOLL_GUTTER_WIDTH               = 50
BUILDCOLL_REMOVEBTN_SIZE             = 34


# ----------------------------------------------------------------------------
# EDIT COLLECTION POPUP
# ----------------------------------------------------------------------------
# 1. Colors
EDITCOLL_BG_COLOR                    = THEME_COLOR4
EDITCOLL_HEADER_TEXT_COLOR           = THEME_COLOR1
EDITCOLL_SUBTEXT_COLOR               = THEME_COLOR1
EDITCOLL_BTN_TEXT_COLOR              = THEME_COLOR5

# 2. Sizes
EDITCOLL_HEADER_PAD_Y_TOP            = 16
EDITCOLL_HEADER_PAD_Y_BOTTOM         = 6
EDITCOLL_HEADER_PAD_X                = 24
EDITCOLL_BTN_PAD_Y                   = 16
EDITCOLL_BTN_PAD_X                   = 10


# ----------------------------------------------------------------------------
# EMPTY STATES (No Books / No Genre)
# ----------------------------------------------------------------------------
# 1. Colors
EMPTYSTATE_NOBOOKS_BG_COLOR          = THEME_COLOR4
EMPTYSTATE_NOGENRE_BG_COLOR          = THEME_COLOR4


# ----------------------------------------------------------------------------
# BOOK DETAIL PAGE
# ----------------------------------------------------------------------------
# 1. Colors - Tag Editing
BOOKDETAIL_TAGHOLDER_BG_COLOR        = THEME_COLOR3
BOOKDETAIL_TAGHOLDER_BORDER_COLOR    = THEME_COLOR4
BOOKDETAIL_TAGHOLDER_SUBTEXT_COLOR   = THEME_COLOR1
BOOKDETAIL_NOTAGS_TEXT_COLOR         = THEME_COLOR9

BOOKDETAIL_TAGEDIT_SYMBOL_COLOR      = THEME_COLOR11
BOOKDETAIL_TAGEDIT_SYMBOL_ONCLICK_COLOR = THEME_COLOR9

BOOKDETAIL_TAGENTRY_TEXT_COLOR       = THEME_COLOR5
BOOKDETAIL_TAGEDIT_XBTN_BG_COLOR     = THEME_COLOR10
BOOKDETAIL_TAGEDIT_XBTN_BORDER_COLOR  = THEME_COLOR1
BOOKDETAIL_TAGEDIT_XSYMBOL_COLOR     = THEME_COLOR5

BOOKDETAIL_TAGSUGGEST_BG_COLOR       = THEME_COLOR4
BOOKDETAIL_TAGSUGGEST_TEXT_COLOR     = THEME_COLOR9
BOOKDETAIL_TAGSUGGEST_HOVER_BG_COLOR = THEME_COLOR1
BOOKDETAIL_TAGSUGGEST_HOVER_TEXT_COLOR = THEME_COLOR2

BOOKDETAIL_TAGSELECT_HOLDER_BG_COLOR = THEME_COLOR2
BOOKDETAIL_TAGSELECT_BG_COLOR        = THEME_COLOR4

# 1. Colors - Tag Display
BOOKDETAIL_TAGDISPLAY_HOLDER_BG_COLOR = THEME_COLOR4
BOOKDETAIL_TAGDISPLAY_LABEL_TEXT_COLOR = THEME_COLOR5
BOOKDETAIL_TAGDISPLAY_SUB_TEXT_COLOR = THEME_COLOR9

BOOKDETAIL_TAGDISPLAY_BG_COLOR       = THEME_COLOR1
BOOKDETAIL_TAGDISPLAY_TEXT_COLOR     = THEME_COLOR4
BOOKDETAIL_TAGDISPLAY_HOVER_BG_COLOR = THEME_COLOR2
BOOKDETAIL_TAGDISPLAY_HOVER_TEXT_COLOR = THEME_COLOR1

# 1. Colors - ISBN
BOOKDETAIL_ISBN_BG_COLOR             = THEME_COLOR4
BOOKDETAIL_ISBN_TEXT_COLOR           = THEME_COLOR5

# 1. Colors - Book Description Card
BOOKDETAIL_CARD_BG_COLOR             = THEME_COLOR2
BOOKDETAIL_CARD_TEXT_COLOR           = THEME_COLOR00

# 2. Sizes - Cover Image
BOOKDETAIL_COVER_XPOS                = 330
BOOKDETAIL_COVER_WIDTH               = 260
BOOKDETAIL_COVER_HEIGHT              = 380
BOOKDETAIL_COVER_GAP                 = 25

# 2. Sizes - Info Card
BOOKDETAIL_CARD_XPOS                 = 840
BOOKDETAIL_CARD_YPOS                 = 460
BOOKDETAIL_CARD_WIDTH                = 640
BOOKDETAIL_CARD_HEIGHT               = 320
BOOKDETAIL_CARD_PAD_X                = 20
BOOKDETAIL_CARD_PAD_Y                = 12

# 2. Sizes - ISBN
BOOKDETAIL_ISBN_YPOS                 = 620

# 2. Sizes - Tags
BOOKDETAIL_TAGS_YPOS                 = 650
BOOKDETAIL_TAGS_LABEL_FONT_SIZE      = 20
BOOKDETAIL_TAGS_FONT_SIZE            = 18

# 2. Sizes - Title/Author/Description Text
BOOKDETAIL_TITLE_FONT_SIZE           = 30
BOOKDETAIL_TITLE_HEIGHT              = 42
BOOKDETAIL_AUTHOR_FONT_SIZE          = 22
BOOKDETAIL_AUTHOR_HEIGHT             = 32
BOOKDETAIL_DESC_FONT_SIZE            = 18
BOOKDETAIL_DESC_MIN_HEIGHT           = 80
BOOKDETAIL_GAP_AFTER_TITLE           = 10
BOOKDETAIL_GAP_AFTER_AUTHOR          = 14

# 2. Sizes - Genre Header
BOOKDETAIL_GENRE_FONT_SIZE           = 48
BOOKDETAIL_GENRE_OFFSET_Y            = 55

# 2. Sizes - Edit Mode Buttons
BOOKDETAIL_EDITBTN_WIDTH             = 150
BOOKDETAIL_EDITBTN_HEIGHT            = 40
BOOKDETAIL_SAVEBTN_OFFSET_X          = 170
BOOKDETAIL_CANCELBTN_OFFSET_X        = 330
BOOKDETAIL_EDITBTN_OFFSET_Y          = 54
BOOKDETAIL_EDITBTN_FONT_SIZE         = 18

# 2. Sizes - Tag Editor
BOOKDETAIL_TAGEDITOR_PLUSBTN_WIDTH   = 34
BOOKDETAIL_TAGEDITOR_ENTRY_WIDTH     = 26
BOOKDETAIL_TAGEDITOR_ENTRY_FONT_SIZE = 14
BOOKDETAIL_TAGEDITOR_PAD_X           = 10
BOOKDETAIL_TAGEDITOR_PAD_Y           = 8
BOOKDETAIL_TAGEDITOR_CHIP_PAD_X      = 6
BOOKDETAIL_TAGEDITOR_CHIP_PAD_Y      = 6


# ----------------------------------------------------------------------------
# CUSTOMIZE GENRES POPUP
# ----------------------------------------------------------------------------
# 1. Colors
GENRESPOP_MAIN_BG_COLOR              = THEME_COLOR1
GENRESPOP_HEADER_BG_COLOR            = THEME_COLOR3
GENRESPOP_LIST_BG_COLOR              = THEME_COLOR2

GENRESPOP_HEADER_TEXT_COLOR          = THEME_COLOR5
GENRESPOP_SUBTEXT_COLOR              = THEME_COLOR4
GENRESPOP_LIST_TEXT_COLOR            = THEME_COLOR5

GENRESPOP_BTN_TEXT_COLOR             = THEME_COLOR5
GENRESPOP_BTN_BG_COLOR               = THEME_COLOR1
GENRESPOP_LIST_BORDER_COLOR          = THEME_COLOR6

GENRESPOP_ADDBTN_BG_COLOR            = THEME_COLOR10
GENRESPOP_ADDBTN_TEXT_COLOR          = THEME_COLOR5

GENRESPOP_ROW_DISABLED_BG_COLOR      = THEME_COLOR1
GENRESPOP_ROW_SELECTED_BG_COLOR      = THEME_COLOR6

# 2. Sizes
GENRESPOP_HEADER_HEIGHT              = 50
GENRESPOP_HEADER_PAD_Y               = 12
GENRESPOP_SUBTEXT_PAD_Y_TOP          = 10
GENRESPOP_SUBTEXT_PAD_Y_BOTTOM       = 5
GENRESPOP_ADD_PAD_X                  = 15
GENRESPOP_ADD_PAD_Y                  = 5
GENRESPOP_ADDBTN_SIZE                = 38
GENRESPOP_LIST_PAD_X                 = 20
GENRESPOP_LIST_PAD_Y                 = 5
GENRESPOP_ROW_PAD_Y                  = 1
GENRESPOP_ROW_PAD_X                  = 5
GENRESPOP_XBTN_SIZE                  = 34
GENRESPOP_FOOTER_PAD_Y               = 10
GENRESPOP_FOOTER_PAD_X               = 20


# ----------------------------------------------------------------------------
# COLLECT MISSING DATA PAGE
# ----------------------------------------------------------------------------
# 1. Colors
MISSINGDATA_CHECKMARK_BG_COLOR       = THEME_COLOR2
MISSINGDATA_CHECKMARK_TEXT_COLOR     = THEME_COLOR5

MISSINGDATA_PLUSUPLOAD_BG                   = THEME_COLOR4
MISSINGDATA_PLUSUPLOAD_BG_ONCLICK_COLOR     = THEME_COLOR1
MISSINGDATA_PLUSUPLOAD_TEXT_COLOR           = THEME_COLOR12
MISSINGDATA_PLUSUPLOAD_TEXT_ONCLICK_COLOR   = THEME_COLOR3

# 2. Sizes
MISSINGDATA_SCROLL_RELWIDTH          = 0.88
MISSINGDATA_SCROLL_RELHEIGHT         = 0.68
MISSINGDATA_SCROLLBAR_WIDTH          = 14
MISSINGDATA_HEADER_HEIGHT            = 70
MISSINGDATA_HEADER_PAD_X             = 12
MISSINGDATA_HEADER_PAD_Y             = 18
MISSINGDATA_ROW_PAD_X                = 12
MISSINGDATA_ROW_PAD_Y                = 10
MISSINGDATA_ENTRY_WIDTH_TITLE        = 18
MISSINGDATA_ENTRY_WIDTH_AUTHOR       = 16
MISSINGDATA_COMBO_WIDTH_GENRE        = 18
MISSINGDATA_PLUSBTN_WIDTH            = 2


# ----------------------------------------------------------------------------
# SYNC LIBRARY PAGE
# ----------------------------------------------------------------------------
# 1. Colors
SYNCLIB_BG_COLOR                     = THEME_COLOR1
SYNCLIB_TEXT_COLOR                   = THEME_COLOR2

def get_user_data_dir(app_name: str = "CozyLibraryManager") -> Path:
    """
    Returns a persistent per-user data directory.
    Windows: %APPDATA%\\CozyLibraryManager
    macOS: ~/Library/Application Support/CozyLibraryManager
    Linux: ~/.local/share/CozyLibraryManager (or $XDG_DATA_HOME)
    """
    sysname = platform.system().lower()

    if sysname == "windows":
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        path = Path(base) / app_name
    elif sysname == "darwin":
        path = Path.home() / "Library" / "Application Support" / app_name
    else:
        base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
        path = Path(base) / app_name

    path.mkdir(parents=True, exist_ok=True)
    return path

class LibraryApp(tk.Tk):

    def _ensure_book_origin(self, book: dict) -> dict:
        """
        If we're already on Book Info and the current payload has an _origin,
        make sure the next book dict keeps that _origin.
        """
        if not isinstance(book, dict):
            return book
        origin = None
        try:
            origin = (getattr(self, 'page_payload', {}) or {}).get('book', {}).get('_origin')
        except Exception:
            origin = None
        if origin and '_origin' not in book:
            b = dict(book)
            b['_origin'] = origin
            return b
        return book

    def _is_windows(self) -> bool:
        return platform.system().lower() == "windows"

    def _broadcast_font_change_windows(self) -> None:
        # HWND_BROADCAST = 0xFFFF, WM_FONTCHANGE = 0x001D
        try:
            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001D, 0, 0,
                0x0002, 1000, None
            )
        except Exception:
            pass

    def _add_private_font_windows(self, font_path: str) -> bool:
        # AddFontResourceExW with FR_PRIVATE makes font available to this process only
        FR_PRIVATE = 0x10
        try:
            add = ctypes.windll.gdi32.AddFontResourceExW
            add.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPVOID]
            added = add(font_path, FR_PRIVATE, None)
            return added > 0
        except Exception:
            return False

    def _load_app_fonts(self) -> None:
        """
        Load fonts from ASSETS/fonts so they work on Windows even if not installed system-wide.
        Safe to call multiple times.
        """
        if not self._is_windows():
            return

        fonts_dir = resource_path("ASSETS", "fonts")  # <-- resource_path returns a Path
        if not fonts_dir.is_dir():
            return

        loaded_any = False
        for fp in fonts_dir.iterdir():
            if fp.suffix.lower() not in (".ttf", ".otf", ".ttc"):
                continue
            if self._add_private_font_windows(str(fp)):
                loaded_any = True

        if loaded_any:
            self._broadcast_font_change_windows()

    def _pick_font_family(self, primary: str, fallbacks: list[str]) -> str:
        """
        Return the first family name that Tk actually sees.
        Keeps casing exactly as Tk reports it.
        """
        fams = tkfont.families(self)  # use this root
        fam_map = {f.lower(): f for f in fams}

        for name in [primary, *fallbacks]:
            if name and name.lower() in fam_map:
                return fam_map[name.lower()]

        return primary

    def _resolve_font_fallbacks(self) -> None:
        global SHARED_FONT_CUSTOM, SHARED_FONT_BUTTON, SHARED_FONT_TABLE
        global SHARED_TABLE_HEADER_FONT, SHARED_TABLE_ROW_FONT
        global ENTRY_BAR_FONT_FAMILY

        SHARED_FONT_TABLE = self._pick_font_family(
            "Liberation Sans",
            ["Cardo", "Cambria", "Segoe UI", "Arial"]
        )
        SHARED_FONT_BUTTON = self._pick_font_family(
            "Sherly Kitchen",
            ["Bebas Neue", "Garamond", "Segoe UI", "Arial"]
        )
        SHARED_FONT_CUSTOM = self._pick_font_family(
            "AESTHICA",
            ["Great Vibes", "Bebas Neue", "Cardo", "Segoe UI"]
        )

        SHARED_TABLE_HEADER_FONT = (SHARED_FONT_TABLE, 20, "bold")
        SHARED_TABLE_ROW_FONT = (SHARED_FONT_TABLE, 16)
        ENTRY_BAR_FONT_FAMILY = SHARED_FONT_TABLE

    def __init__(self) -> None:
        super().__init__()

        # prevent initial "flash" before first page is fully rendered
        self.withdraw()

        # Load bundled fonts (Windows) + resolve primary->fallback font families
        self._load_app_fonts()
        self._resolve_font_fallbacks()

        # Build Tk Font objects using the resolved families
        self._init_fonts()

        self.title(SHARED_WINDOW_TITLE)
        self.minsize(900, 600)
        self.geometry("1280x920")

        self.active_widgets: list[tk.Widget] = []
        self.placed_widgets: list[tuple[tk.Widget, int, int, str]] = []
        self.canvas_text_items: list[tuple[int, float, float]] = []

        # --- canvas ---
        self.canvas = tk.Canvas(
            self,
            width=SHARED_WINDOW_DESIGN_WIDTH,
            height=SHARED_WINDOW_DESIGN_HEIGHT,
            highlightthickness=0,
            bd=0,
            bg=BROWSEGENRES_GRID_BG_COLOR,
        )
        self.canvas.pack(fill="both", expand=True)
        self.page_payload: dict[str, Any] = {}

        self._bg_pil: Image.Image | None = None
        self._bg_tk: ImageTk.PhotoImage | None = None
        self._scroll_target: tk.Canvas | None = None
        self._resize_after_id: str | None = None

        style = ttk.Style(self)
        style.theme_use("clam")

        # ---------- SIDE MENU (pause-style overlay) ----------
        self._side_menu_win: tk.Toplevel | None = None
        self._side_menu_pil: Image.Image | None = None
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self._side_menu_open = False
        self._side_menu_frame: tk.Frame | None = None
        self._side_menu_bg_lbl: tk.Label | None = None
        self._side_menu_bg_pil: Image.Image | None = None
        self._side_menu_bg_tk: ImageTk.PhotoImage | None = None
        self._side_menu_bg_last_size: tuple[int, int] | None = None
        self._side_menu_dim: tk.Toplevel | None = None
        self._side_menu_panel_win: tk.Toplevel | None = None

        self._menu_btn_lbl: tk.Label | None = None
        self._menu_btn_pil: Image.Image | None = None
        self._menu_btn_tk: ImageTk.PhotoImage | None = None
        self._menu_btn_last_size: int | None = None
        self._menu_btn_item: int | None = None

        self._init_side_menu_assets()

        self._load_background_image()
        self._page_img_refs: list[ImageTk.PhotoImage] = []
        self._sync_popup_open = False

        self.bind_all("<MouseWheel>", self._on_global_mousewheel)
        self.bind_all("<Button-4>", self._on_global_mousewheel)
        self.bind_all("<Button-5>", self._on_global_mousewheel)
        self.bind_all("<Escape>", self._escape_exit_fullscreen, add="+")
        self.bind("<Command-f>", lambda e: self.toggle_fullscreen())

        self._page_rebuild_after_id = None
        self.current_page: str = "main"
        self._nav_history: list[tuple[str, dict]] = []
        self._nav_suppress_record = False

        self._mark_read_mode: bool = False
        self._collection_read_marks: dict[str, set[str]] = {}  # collection_name -> set(book_key)
        # ---------- BOOK DETAIL EDIT MODE ----------
        self._book_edit_mode: bool = False
        self._book_edit_vars: dict[str, Any] = {}
        self._current_book_detail: dict | None = None

        # ---------- SIDE MENU BUTTON MAP ----------
        # Each entry: "page_name": [("Button Label", callable), ...]
        # If a page maps to [], the side menu shows ONLY the background.
        self.side_menu_map: dict[str, list[tuple[str, Callable[[], Any]]]] = {
            "main": [
                ("View Collections", self.show_collections_page),
                ("Browse by Genre", lambda: self.show_browse_genres_page("all")),
                ("Settings", self.show_settings_page),
            ],
            "browse_genres": [
                ("Customize Genres", self._show_customize_genres_popup),
                ("View Collections", self.show_collections_page),
                ("Settings", self.show_settings_page),
            ],
            "genre_page": [
                ("Browse Genres", lambda: self.show_browse_genres_page(self.page_payload.get("tab", "all"))),
                ("View Collections", self.show_collections_page),
                ("Settings", self.show_settings_page),
            ],
            "tag_page": [
                ("Browse Genres", lambda: self.show_browse_genres_page("all")),
                ("Settings", self.show_settings_page),
            ],
            "search_results": [
                ("Browse Genres", lambda: self.show_browse_genres_page("all")),
                ("View Collections", self.show_collections_page),
                ("Settings", self.show_settings_page),
            ],
            "missing_values": [
                ("View Collections", self.show_collections_page),
                ("Settings", self.show_settings_page),
            ],
            "book_detail": [
                ("Edit Book Details", self._side_edit_book_details),
                ("Add to Collection", self._side_add_to_collection),
                ("Browse Genres", lambda: self.show_browse_genres_page("all")),
                ("Settings", self.show_settings_page),
            ],
            "collections": [
                ("Add New", self.show_build_collection_page),
                ("Edit Collections", self._side_edit_collections),
                ("Settings", self.show_settings_page),
            ],
            "open_collection": [
                ("Edit Collection", self._side_edit_open_collection),
                ("Mark As Read", self._side_toggle_mark_as_read),
                ("Settings", self.show_settings_page),
            ],
            "build_collection": [
                ("Duplicate Collection", self._side_duplicate_collection),
                ("Settings", self.show_settings_page),
            ],
        }

        # --- collections (in-memory for now) ---
        self._build_collection_selected: list[str] = []
        self.data = LibraryData(get_user_data_dir())

        # Your UI continues to use a list of dicts
        self.catalog = list(self.data.catalog.values())

        self.last_search_results: list[dict] | None = None
        self.last_search_query: str = ""
        self.show_main_page()
        self.update_idletasks()
        self._update_background_image()
        self._update_canvas_text_positions()
        self._reposition_design_widgets()
        self.after(50, lambda: (self.deiconify(), self.lift()))

    def _safe_call(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            # If app is closing/destroyed, don't try to show a Tk messagebox.
            try:
                if self.winfo_exists():
                    messagebox.showerror("Error", str(e), parent=self)
            except tk.TclError:
                pass
    def _on_canvas_configure(self, event):
        # keep floating UI (menu button) anchored during live resize
        self._position_menu_button()
    def _cancel_pending_page_jobs(self):
        # cancels BOTH background resize and page rebuild callbacks
        for attr in ("_resize_after_id", "_page_rebuild_after_id"):
            after_id = getattr(self, attr, None)
            if after_id is not None:
                try:
                    self.after_cancel(after_id)
                except Exception:
                    pass
                setattr(self, attr, None)
    def toggle_fullscreen(self, on: bool | None = None):
        if on is None:
            on = not bool(self.attributes("-fullscreen"))

        self.attributes("-fullscreen", on)
        self.after(50, self._force_front)

        # Reset Browse Genres "wide-mode memory" when leaving fullscreen
        if not on:
            self._browse_is_wide = None
            self._browse_last_canvas_w = None
            self._browse_render_after_id = None

        def _refresh():
            page = getattr(self, "current_page", "")
            payload = getattr(self, "page_payload", {}) or {}

            # This is a rebuild, not real navigation
            self._nav_suppress_record = True

            if page == "browse_genres":
                self.show_browse_genres_page(payload.get("tab", "fiction"))

            elif page == "genre_page":
                self.show_genre_page(payload.get("genre", ""))

            elif page == "collections":
                self.show_collections_page()


            elif page == "search_results":
                if self.last_search_results is not None:
                    self.show_search_results(self.last_search_results, original_query=self.last_search_query)

            elif page == "book_detail":
                book = payload.get("book")
                if book:
                    self.show_book_detail(book)

            else:
                self.show_main_page()

        self.after(180, _refresh)
    def _escape_exit_fullscreen(self, _evt=None):
        """Escape key: always return to standard window size from fullscreen/zoomed."""
        # Turn off true fullscreen (works on many setups)
        try:
            if bool(self.attributes("-fullscreen")):
                self.toggle_fullscreen(False)
        except Exception:
            pass

        # Also handle "zoomed"/maximized state (common on Windows)
        try:
            if self.state() == "zoomed":
                self.state("normal")
        except Exception:
            pass

        return "break"
    def _force_front(self):
        try:
            self.deiconify()  # un-minimize if needed
            self.lift()  # bring to front
            self.focus_force()  # grab focus
            self.attributes("-topmost", True)
            self.after(100, lambda: self.attributes("-topmost", False))
        except Exception:
            pass
    def gui_factory_reset(self):
        # 1) first confirmation
        ok = messagebox.askyesno(
            "Factory Reset",
            "This will DELETE ALL library data and customizations, including:\n"
            "- your catalog\n"
            "- cached covers\n"
            "- genres/tags/shelves/collections/settings (anything stored by the app)\n\n"
            "This cannot be undone.\n\n"
            "Tip: Export CSV first if you want a backup.\n\n"
            "Continue?"
        )
        if not ok:
            return

        # 2) typed confirmation
        typed = simpledialog.askstring(
            "Confirm Factory Reset",
            'Type RESET to permanently delete your library data:'
        )
        if typed != "RESET":
            messagebox.showinfo("Canceled", "Factory reset canceled.")
            return

        # Do it
        try:
            self.data.factory_reset()
            self.data.save()
            self._refresh_catalog_from_data()
        except Exception as e:
            messagebox.showerror("Factory Reset Failed", str(e))
            return

        messagebox.showinfo("Factory Reset Complete", "Library data was wiped and reset.")
        self.show_main_page()

    # ---------- LOGIC: CATALOG ----------
    def load_catalog(self, csv_path: Path) -> list[dict]:
        import csv
        items: list[dict] = []
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(row)
        return items
    def _refresh_catalog_from_data(self):
        self.catalog = list(self.data.catalog.values())
    def gui_import_csv(self):
        path = filedialog.askopenfilename(
            title="Import Library CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return

        # Quick UI feedback immediately
        self.config(cursor="watch")
        self.update_idletasks()

        def worker():
            try:
                report = self.data.import_csv(
                    Path(path),
                    add_new_isbn_only=True,
                    require_isbn=True,
                )

                def done_ui():
                    self.config(cursor="")
                    self._refresh_catalog_from_data()
                    messagebox.showinfo(
                        "Import complete",
                        f"Imported rows: {report.imported}\n"
                        f"Created new (new ISBNs): {report.created}\n"
                        f"Skipped (no ISBN): {getattr(report, 'skipped_no_isbn', 0)}\n"
                        f"Skipped (ISBN already exists): {getattr(report, 'skipped_existing_isbn', 0)}"
                    )
                    self.show_all_books_page()

                self.after(0, done_ui)

            except Exception as e:
                def fail_ui():
                    self.config(cursor="")
                    messagebox.showerror("Import failed", str(e))

                self.after(0, fail_ui)

        threading.Thread(target=worker, daemon=True).start()
    def gui_export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Export Library CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        try:
            self.data.export_csv(Path(path))
            messagebox.showinfo("Export complete", "Your library was exported successfully.")
        except Exception as e:
            messagebox.showerror("Export failed", str(e))
    def gui_download_missing_covers(self):
        if getattr(self, "_sync_popup_open", False):
            return

        # Create ONE popup, once.
        try:
            win = tk.Toplevel(self)
        except Exception as e:
            self._sync_popup_open = False
            try:
                self._btn_sync.config(state="normal")
            except Exception:
                pass
            messagebox.showerror("Sync failed", str(e))
            return

        # ONLY set the flag after the Toplevel exists
        self._sync_popup_open = True

        try:
            self._btn_sync.config(state="disabled")
        except Exception:
            pass

        win.title("Syncing Library")
        win.resizable(False, False)

        POP_BG = SYNCLIB_BG_COLOR
        POP_FG = SYNCLIB_TEXT_COLOR
        TITLE_FONT = (SHARED_FONT_CUSTOM, 20, "bold")
        BODY_FONT = (SHARED_FONT_CUSTOM, 14)

        # ----- phase + animated dots -----
        phase = {"mode": "sorting"}  # "sorting" or "updating"
        dots_state = {"n": 0, "after_id": None}

        status_var = tk.StringVar(value="Starting…")
        pct_var = tk.StringVar(value="0 / 0")

        # ttk progress styling
        style = ttk.Style(win)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Cover.Horizontal.TProgressbar",
            troughcolor=POP_BG,
            background=POP_FG,
            thickness=18,
        )

        win.configure(bg=POP_BG)
        win.transient(self)
        win.grab_set()

        header = tk.Label(win, text="Syncing Library", bg=POP_BG, fg=POP_FG, font=TITLE_FONT)
        header.pack(pady=(16, 6))

        bar = ttk.Progressbar(
            win, orient="horizontal", length=560,
            mode="determinate", style="Cover.Horizontal.TProgressbar"
        )
        bar.pack(pady=(6, 10))

        lbl = tk.Label(
            win, textvariable=status_var, bg=POP_BG, fg=POP_FG,
            font=BODY_FONT, anchor="w", justify="left", wraplength=560
        )
        lbl.pack(fill="x", padx=24)

        lbl2 = tk.Label(win, textvariable=pct_var, bg=POP_BG, fg=POP_FG, font=BODY_FONT, anchor="w")
        lbl2.pack(fill="x", padx=24, pady=(4, 0))

        # ----- stop/cancel state -----
        state = {"stop": False, "save": False, "cancel": False}

        # Snapshot existing cover files so we can delete any new ones on Cancel
        try:
            existing_files = {p.name for p in self.data.covers_dir.glob("*") if p.is_file()}
        except Exception:
            existing_files = set()

        # Snapshot cover_index so Cancel can fully revert (prevents stale index entries)
        try:
            existing_cover_index = dict(getattr(self.data, "cover_index", {}) or {})
        except Exception:
            existing_cover_index = {}


        def start_sorting_animation():
            phase["mode"] = "sorting"
            bar.config(mode="indeterminate")
            bar.start(12)
            pct_var.set("")  # hide count during sorting

            def tick():
                if not win.winfo_exists():
                    return
                dots_state["n"] = (dots_state["n"] + 1) % 4
                status_var.set("Sorting library" + ("." * dots_state["n"]))
                dots_state["after_id"] = win.after(350, tick)

            tick()

        def stop_sorting_animation():
            if dots_state["after_id"] is not None:
                try:
                    win.after_cancel(dots_state["after_id"])
                except Exception:
                    pass
                dots_state["after_id"] = None
            try:
                bar.stop()
            except Exception:
                pass
            bar.config(mode="determinate")

        def close_popup_now():
            self._sync_popup_open = False
            try:
                self._btn_sync.config(state="normal")
            except Exception:
                pass
            try:
                stop_sorting_animation()
            except Exception:
                pass
            try:
                win.grab_release()
            except Exception:
                pass
            try:
                if win.winfo_exists():
                    win.destroy()
            except Exception:
                pass

        def do_cancel():
            state["stop"] = True
            state["cancel"] = True
            state["save"] = False
            try:
                btn_cancel.config(state="disabled")
                btn_save.config(state="disabled")
            except Exception:
                pass
            close_popup_now()

        def do_stop_save():
            state["stop"] = True
            state["save"] = True
            state["cancel"] = False
            try:
                btn_cancel.config(state="disabled")
                btn_save.config(state="disabled")
            except Exception:
                pass
            close_popup_now()

        # Buttons
        btn_row = tk.Frame(win, bg=POP_BG)
        btn_row.pack(pady=16)

        btn_cancel = tk.Button(
            btn_row,
            text="Cancel (no save)",
            command=do_cancel,
            bg=SHARED_BUTTON1_TEXT_COLOR, fg=SHARED_BUTTON1_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            borderwidth=SHARED_BUTTON_BORDER_WIDTH,
            font=(SHARED_FONT_CUSTOM, 14),
            highlightthickness=0,
            relief="flat",
            takefocus=False,
            padx=14, pady=6,
        )
        btn_cancel.pack(side="left", padx=10)

        btn_save = tk.Button(
            btn_row,
            text="Stop & Save",
            command=do_stop_save,
            bg=SHARED_BUTTON1_TEXT_COLOR, fg=SHARED_BUTTON1_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            borderwidth=SHARED_BUTTON_BORDER_WIDTH,
            font=(SHARED_FONT_CUSTOM, 14),
            highlightthickness=0,
            relief="flat",
            takefocus=False,
            padx=14, pady=6,
        )
        btn_save.pack(side="left", padx=10)

        win.bind("<Escape>", lambda e: do_cancel())
        win.protocol("WM_DELETE_WINDOW", do_cancel)

        # Center it
        win.update_idletasks()
        w, h = 620, 260
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        # ---- FORCE THE POPUP TO ACTUALLY APPEAR NOW ----
        win.deiconify()
        win.lift()
        win.focus_force()
        try:
            win.attributes("-topmost", True)
            win.after(120, lambda: win.attributes("-topmost", False))
        except Exception:
            pass

        start_sorting_animation()
        win.update_idletasks()
        win.update()  # flush draw

        switched = {"done": False}

        def progress_cb(current, total_n, msg):
            def _ui():
                if not win.winfo_exists():
                    return
                if (not switched["done"]) and current > 0:
                    switched["done"] = True
                    try:
                        bar.stop()
                    except Exception:
                        pass
                    bar.config(mode="determinate")
                    bar["maximum"] = max(total_n, 1)

                if bar.cget("mode") == "determinate":
                    bar["value"] = current

                status_var.set(msg)
                pct_var.set(f"{current} / {total_n}")

            self.after(0, _ui)

        def stop_flag():
            return state["stop"]

        def worker():
            try:
                # SORT PHASE (local + fast)
                self.data.rebuild_queues()

                if stop_flag():
                    self.after(0, lambda: (stop_sorting_animation(), win.winfo_exists() and win.destroy()))
                    return

                books = self.data.get_books_needing_update()

            except Exception as e:
                def fail_ui():
                    if win.winfo_exists():
                        win.destroy()
                    self._sync_popup_open = False
                    try:
                        self._btn_sync.config(state="normal")
                    except Exception:
                        pass
                    messagebox.showerror("Sync failed", str(e))

                self.after(0, fail_ui)
                return

            if not books:
                def nothing_ui():
                    stop_sorting_animation()
                    if win.winfo_exists():
                        win.destroy()
                    self._sync_popup_open = False
                    try:
                        self._btn_sync.config(state="normal")
                    except Exception:
                        pass

                    messagebox.showinfo("Nothing to update", "No books currently need updating.")

                self.after(0, nothing_ui)
                return

            total = len(books)

            def start_update_ui():
                stop_sorting_animation()
                bar["maximum"] = max(total, 1)
                bar["value"] = 0
                pct_var.set(f"0 / {total}")
                status_var.set("Starting update…")
                bar.config(mode="indeterminate")
                bar.start(12)

            self.after(0, start_update_ui)

            stats = self.data.sync_missing_data(
                books,
                progress_cb=progress_cb,
                stop_flag=stop_flag,
                polite_delay=0.0,
                max_workers=8,
            )

            def done_ui():
                if win.winfo_exists():
                    win.destroy()
                self._sync_popup_open = False
                try:
                    self._btn_sync.config(state="normal")
                except Exception:
                    pass

                if state["cancel"]:
                    # delete any new covers downloaded during this run
                    try:
                        for p in self.data.covers_dir.glob("*"):
                            if p.is_file() and p.name not in existing_files:
                                try:
                                    p.unlink()
                                except Exception:
                                    pass
                    except Exception:
                        pass

                    # Revert any in-memory/disk cover_index changes from this run
                    try:
                        self.data.cover_index = dict(existing_cover_index)
                        self.data.save()  # writes cover_index.json back to the same data_dir
                        self._refresh_catalog_from_data()
                    except Exception:
                        pass

                    messagebox.showinfo("Canceled", "Canceled. No progress was saved.")
                    return

                try:
                    self.data.save()
                    self._refresh_catalog_from_data()
                except Exception:
                    pass

                messagebox.showinfo(
                    "Update complete",
                    f"Downloaded: {stats['downloaded']}\n"
                    f"Skipped: {stats['skipped']}\n"
                    f"Failed: {stats['failed']}\n"
                    f"Enriched: {stats.get('enriched', 0)}"
                )

                # After sync, show a review page for any remaining missing values
                try:
                    if self._books_with_missing_values():
                        self.show_missing_values_page()
                except Exception:
                    pass

            self.after(0, done_ui)

        # IMPORTANT: start the worker AFTER Tk gets a chance to paint the popup
        self.after(50, lambda: threading.Thread(target=worker, daemon=True).start())
    def _books_with_missing_values(self) -> list[dict]:
        """
        Books that still have missing/placeholder metadata after sync.

        IMPORTANT:
        This review focuses on the fields you actually collect on the Missing Data Review page:
        - Cover image
        - Genre

        (Title/author are still treated as missing if blank, but we do NOT block on ISBN/description
        so the review page doesn't incorrectly show every synced book.)
        """
        missing: list[dict] = []
        for b in (self.catalog or []):
            if not isinstance(b, dict):
                continue
            bid = (b.get("book_id") or "").strip()
            if not bid:
                continue

            title = self._mdr_title_display(b)
            author = self._mdr_author_display(b)
            genre = (b.get("genre") or "").strip()

            # cover check
            cover_ok = False
            try:
                cover_ok = bool(self.data.get_cover_path(bid))
            except Exception:
                cover_ok = False

            # treat blank/placeholder as missing
            bad_genre = self._is_bad_genre(genre)
            if (not cover_ok) or bad_genre or (not title) or (not author):
                missing.append(b)

        # stable sort: most-missing first by simple score, then title
        def score(b: dict) -> tuple[int, str]:
            bid = (b.get("book_id") or "").strip()
            title = self._mdr_title_display(b)
            author = self._mdr_author_display(b)
            genre = (b.get("genre") or "").strip()
            cover_ok = False
            try:
                cover_ok = bool(self.data.get_cover_path(bid))
            except Exception:
                cover_ok = False

            bad_genre = self._is_bad_genre(genre)
            s = 0
            s += 1 if not cover_ok else 0
            s += 1 if bad_genre else 0
            s += 1 if not title else 0
            s += 1 if not author else 0

            return (-s, title.lower())

        missing.sort(key=score)
        return missing
    def show_missing_values_page(self):
        """
        Post-sync review page: lists ONLY books that are still missing values after sync,
        and lets the user fill them inline (genre dropdown, optional text, and cover upload).
        """
        self.set_page("missing_values")
        self.clear_page()
        # Reuse an existing background (no custom asset required)
        self.set_background(SHOW_BOOKS_BG_IMG)

        # Title
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=50, weight="bold")
        self.make_canvas_text(
            "Missing Data Review",
            0.5,
            0.16,
            title_font,
        )

        subtitle_font = tkfont.Font(family=SHARED_FONT_TABLE, size=18, weight="bold")
        self.make_canvas_text(
            "Add missing info below, then click SAVE (bottom-left).",
            0.5,
            0.22,
            subtitle_font,
        )

        books = self._books_with_missing_values()
        # If nothing missing, take user back to Home (or main menu)
        if not books:
            self.show_main_page()
        # Editable review UI
        self._make_missing_data_review_card(books)

        # Left nav: SAVE must stack above BACK, and BACK above HOME
        # ✅ Use make_left_nav_stack(above=...) to ensure correct stacking.
        self.make_left_nav_stack(
            above=[("Save", self._save_missing_data_review)],
            home_text="Home",
            home_cmd=getattr(self, "go_home", None),
        )

    # ------------------------------
    # Missing Data Review helpers
    # ------------------------------
    _MDR_GENRE_PLACEHOLDER = "select genre"
    _MDR_ADD_GENRE_OPTION = "Add new genre…"

    def _add_recent_search(self, term: str, *, max_keep: int = 12):
        term = (term or "").strip()
        if not term:
            return
        recent = getattr(self, "_recent_searches", [])
        if not isinstance(recent, list):
            recent = []
        # dedupe (case-insensitive), move to front
        recent = [r for r in recent if (r or "").strip().lower() != term.lower()]
        recent.insert(0, term)
        self._recent_searches = recent[:max_keep]
    def _get_recent_searches(self, limit: int = 6) -> list[str]:
        recent = getattr(self, "_recent_searches", [])
        if not isinstance(recent, list):
            return []
        out = []
        seen = set()
        for r in recent:
            s = (r or "").strip()
            if s and s.lower() not in seen:
                seen.add(s.lower())
                out.append(s)
            if len(out) >= limit:
                break
        return out
    def _mdr_unescape(self, s: str) -> str:
        """HTML-unescape a string safely (OpenLibrary sometimes returns entities in title/author)."""
        try:
            return html.unescape(s or "")
        except Exception:
            return (s or "")
    def _mdr_title_display(self, b: dict) -> str:
        return self._mdr_unescape((b.get("title") or "").strip())
    def _mdr_author_display(self, b: dict) -> str:
        """Best-effort author display consistent with other UI pages."""
        raw = (b.get("author") or "").strip()
        if raw:
            return self._mdr_unescape(raw)
        return self._mdr_unescape(self._format_author_display(b, "first_last"))
    def _missing_review_flags(self, books: list[dict]) -> tuple[bool, bool, bool, bool]:
        """Return which columns should be shown: (show_title, show_author, show_genre, show_cover)."""
        show_title = False
        show_author = False
        show_genre = False
        show_cover = False

        for b in (books or []):
            if not isinstance(b, dict):
                continue
            bid = (b.get("book_id") or "").strip()
            if not bid:
                continue

            title = self._mdr_title_display(b)
            author = self._mdr_author_display(b)
            genre = (b.get("genre") or "").strip()

            if not title:
                show_title = True
            if not author:
                show_author = True

            bad_genre = self._is_bad_genre(genre)
            if bad_genre:
                show_genre = True

            cover_ok = False
            try:
                cover_ok = bool(self.data.get_cover_path(bid))
            except Exception:
                cover_ok = False
            if not cover_ok:
                show_cover = True

        return show_title, show_author, show_genre, show_cover
    def _missing_review_genre_choices(self) -> list[str]:
        """Build genre list for dropdowns using data layer as single source of truth."""
        # Use data layer's get_all_active_genres() - handles standard genres 
        # (with renames applied, excluding deleted) plus custom genres
        base = self.data.get_all_active_genres()
        
        # Placeholder first; add-genre option last
        return [self._MDR_GENRE_PLACEHOLDER, *base, self._MDR_ADD_GENRE_OPTION]
    def _missing_review_upload_cover(self, book_id: str) -> None:
        """Upload cover and refresh missing values page."""
        self._prompt_and_upload_cover(book_id, refresh_callback=self.show_missing_values_page)
    def _make_missing_data_review_card(self, books: list[dict]) -> None:
        """Scrollable editable table for the Missing Data Review page."""
        # Reset per-page state
        self._missing_review_vars: dict[str, dict[str, object]] = {}

        show_title, show_author, show_genre, show_cover = self._missing_review_flags(books)

        # Nothing to show? (Shouldn't happen if books list is non-empty)
        if not (show_title or show_author or show_genre or show_cover):
            show_genre = True
            show_cover = True

        container, canvas, scroll_frame = self._make_scroll_container(
            bg=SHARED_SCROLL_BG_COLOR,
            relwidth=0.88,
            relheight=0.68,
            top_inset=70,
            sb_width=14,
            content_pad_x=0,
            content_pad_y=0,
        )

        # Pinned header row
        header = tk.Frame(container, bg=SHARED_MAINHEADER2_BG_COLOR, height=70, highlightthickness=0, bd=0)
        header.place(x=0, y=0, relwidth=1.0, height=70)
        header.pack_propagate(False)
        self.active_widgets.append(header)

        # Column model
        cols: list[tuple[str, int, int]] = []
        cols.append(("Book", 420, 0))  # (label, minwidth, weight)

        if show_title:
            cols.append(("Title", 240, 0))
        if show_author:
            cols.append(("Author", 220, 0))
        if show_genre:
            cols.append(("Genre", 220, 0))

        # Spacer pushes the cover column to the far right edge (near scrollbar)
        if show_cover:
            cols.append(("", 1, 1))      # spacer
            cols.append(("Cover", 70, 0))  # + button column

        # Header grid
        for ci, (label, minw, weight) in enumerate(cols):
            header.grid_columnconfigure(ci, minsize=minw, weight=weight)
            if not label:
                continue
            tk.Label(
                header,
                text=label,
                bg=SHARED_MAINHEADER2_BG_COLOR,
                fg=SHARED_MAINHEADER2_TEXT_COLOR,
                font=(SHARED_FONT_TABLE, 18, "bold"),
                anchor="w",
            ).grid(row=0, column=ci, sticky="w", padx=(12 if ci == 0 else 8), pady=18)

        # Body rows
        genre_choices = self._missing_review_genre_choices() if show_genre else []
        def _ellipsize(s: str, max_chars: int) -> str:
            s = (s or "").strip()
            if len(s) <= max_chars:
                return s
            return (s[: max(0, max_chars - 1)].rstrip() + "…")

        book_wrap = max(120, cols[0][1] - 24)


        for r, b in enumerate(books):
            if not isinstance(b, dict):
                continue
            bid = (b.get("book_id") or "").strip()
            if not bid:
                continue

            row_bg = SHARED_TABLE2_ALTROW_BG_COLOR if (r % 2 == 0) else SHARED_TABLE2_BG_COLOR
            row = tk.Frame(scroll_frame, bg=row_bg, highlightthickness=0, bd=0)
            row.grid(row=r, column=0, sticky="ew")
            self.active_widgets.append(row)

            for ci, (_label, minw, weight) in enumerate(cols):
                row.grid_columnconfigure(ci, minsize=minw, weight=weight)

            # base info (normalize + HTML-unescape for display)
            title = self._mdr_title_display(b)
            author = self._mdr_author_display(b)
            year = self._mdr_unescape((b.get("year") or "").strip())

            title_line = _ellipsize(title, 70) if title else "Missing title"
            base_txt = title_line

            if author:
                base_txt += f"\nby {_ellipsize(author, 55)}"
            else:
                base_txt += "\nby Missing author"

            if year:
                base_txt += f"  ({_ellipsize(year, 10)})"

            tk.Label(
                row,
                text=base_txt,
                justify="left",
                bg=row_bg,
                fg=SHARED_SCROLLROW2_TEXT_COLOR,
                font=(SHARED_FONT_TABLE, 14, "bold" if title else "normal"),
                anchor="w",
                wraplength=book_wrap,
            ).grid(row=0, column=0, sticky="w", padx=(12, 8), pady=10)

            c = 1
            row_vars: dict[str, object] = {"book_id": bid, "row_bg": row_bg}

            # Optional title entry
            if show_title:
                tvar = tk.StringVar(value=title)
                ent = tk.Entry(
                    row,
                    textvariable=tvar,
                    font=(SHARED_FONT_TABLE, 14),
                    width=18,
                    bg=SHARED_ENTRY1_BG_COLOR,
                    fg=SHARED_ENTRY1_TEXT_COLOR,
                    insertbackground=SHARED_ENTRY1_BG_COLOR,
                )

                ent.grid(row=0, column=c, sticky="w", padx=8, pady=10)
                row_vars["title_var"] = tvar
                c += 1

            # Optional author entry
            if show_author:
                avar = tk.StringVar(value=author)
                ent = tk.Entry(
                    row,
                    textvariable=avar,
                    font=(SHARED_FONT_TABLE, 14),
                    width=16,
                    bg=SHARED_ENTRY2_BG_COLOR,
                    fg=SHARED_ENTRY2_TEXT_COLOR,
                    insertbackground=SHARED_ENTRY_CURSOR_COLOR,
                )
                ent.grid(row=0, column=c, sticky="w", padx=8, pady=10)
                row_vars["author_var"] = avar
                c += 1

            # Genre dropdown (available for all rows when any genre is missing)
            if show_genre:
                raw_g = (b.get("genre") or "").strip()
                bad_g = self._is_bad_genre(raw_g)
                initial = self._MDR_GENRE_PLACEHOLDER if bad_g else raw_g.strip().title()

                gvar = tk.StringVar(value=initial)
                combo = ttk.Combobox(
                    row,
                    textvariable=gvar,
                    values=genre_choices,
                    state="readonly",
                    font=(SHARED_FONT_TABLE, 14),
                    width=18,
                )
                combo.grid(row=0, column=c, sticky="w", padx=8, pady=10)
                row_vars["genre_var"] = gvar
                c += 1

            # Spacer + Cover upload
            if show_cover:
                # if spacer exists, it is at column c (before cover)
                spacer_ci = len(cols) - 2
                cover_ci = len(cols) - 1

                # Cover status
                cover_ok = False
                try:
                    cover_ok = bool(self.data.get_cover_path(bid))
                except Exception:
                    cover_ok = False

                if cover_ok:
                    tk.Label(
                        row,
                        text="✓",
                        bg=row_bg,
                        fg=MISSINGDATA_CHECKMARK_TEXT_COLOR,
                        font=(SHARED_FONT_TABLE, 18, "bold"),
                        anchor="e",
                    ).grid(row=0, column=cover_ci, sticky="e", padx=(8, 14), pady=10)
                else:
                    tk.Button(
                        row,
                        text="+",
                        command=lambda _bid=bid: self._missing_review_upload_cover(_bid),
                        font=(SHARED_FONT_TABLE, 18, "bold"),
                        bg=MISSINGDATA_PLUSUPLOAD_BG,
                        fg=MISSINGDATA_PLUSUPLOAD_TEXT_COLOR,
                        activebackground=MISSINGDATA_PLUSUPLOAD_BG_ONCLICK_COLOR,
                        activeforeground=MISSINGDATA_PLUSUPLOAD_TEXT_ONCLICK_COLOR,
                        bd=SHARED_BUTTON_BORDER_WIDTH,
                        relief="flat",
                        cursor="hand2",
                        highlightthickness=0,
                        width=2,
                    ).grid(row=0, column=cover_ci, sticky="e", padx=(8, 14), pady=10)

            self._missing_review_vars[bid] = row_vars

        # Ensure width sync after population
        try:
            canvas.after_idle(lambda: canvas.configure(scrollregion=canvas.bbox("all")))
        except Exception:
            pass
    def _save_missing_data_review(self) -> None:
        """Persist changes made on the Missing Data Review page."""
        rows = getattr(self, "_missing_review_vars", None)
        if not isinstance(rows, dict) or not rows:
            return

        changed = 0
        for bid, row in rows.items():
            if not isinstance(row, dict):
                continue
            latest = self.data.get_book(bid) or {}
            if not isinstance(latest, dict):
                latest = {}

            updated: dict[str, object] = {}

            # title/author optional
            tvar = row.get("title_var")
            if isinstance(tvar, tk.StringVar):
                new_t = (tvar.get() or "").strip()
                if new_t:
                    updated["title"] = new_t

            avar = row.get("author_var")
            if isinstance(avar, tk.StringVar):
                new_a = (avar.get() or "").strip()
                if new_a:
                    updated["author"] = new_a
                    updated["creators"] = new_a

            # genre
            gvar = row.get("genre_var")
            if isinstance(gvar, tk.StringVar):
                g = (gvar.get() or "").strip()
                if g == self._MDR_ADD_GENRE_OPTION:
                    new_g = simpledialog.askstring("Add Genre", "Enter new genre name:")
                    if new_g:
                        g = new_g.strip().title()
                        try:
                            self.data.add_user_genre(g)
                        except Exception:
                            pass
                    else:
                        g = self._MDR_GENRE_PLACEHOLDER

                if g and g != self._MDR_GENRE_PLACEHOLDER:
                    updated["genre"] = g
                else:
                    # placeholder means "no selection" — don't overwrite an existing real genre
                    existing = (latest.get("genre") or "").strip()
                    if self._is_bad_genre(existing):
                        # keep missing (blank) so it stays on this page until user selects
                        updated["genre"] = ""

            if updated:
                latest.update(updated)
                self.data.catalog[bid] = latest
                changed += 1

        # Persist once
        try:
            self.data.save()
        except Exception as e:
            messagebox.showerror("Save", f"Could not save changes.\n\n{e}")
            return

        # Refresh UI cache and re-render review (so completed rows disappear)
        try:
            self.catalog = list(self.data.catalog.values())
        except Exception:
            pass

        try:
            messagebox.showinfo("Save", "Saved.")
        except Exception:
            pass

        self.show_missing_values_page()

    # Centralized bad genre values for consistent checking
    _BAD_GENRE_VALUES = frozenset({"unknown", "unassigned", "none", "n/a", "na", ""})

    def _is_bad_genre(self, genre: str | None) -> bool:
        """Check if a genre value is missing or a placeholder."""
        g = (genre or "").strip().lower()
        return g in self._BAD_GENRE_VALUES
    def _norm_genre(self, g: str) -> str:
        g = (g or "").strip()
        return g if g else "Unknown"
    def _make_genre_header_row(self, parent: tk.Widget, text: str, cols: int, bg: str = SHARED_TABLE_BG_COLOR, fg: str = "SHARED_SCROLLROW_TEXT_COLOR") -> tk.Frame:
        """
        Short header row used ONLY in grid view when sorting by genre.
        """
        row = tk.Frame(parent, bg=bg, highlightthickness=0, bd=0, height=28)
        row.grid_columnconfigure(0, weight=1)

        lbl = tk.Label(
            row,
            text=text.upper(),
            bg=SHARED_TABLE_BG_COLOR,
            fg=SHARED_SCROLLROW_TEXT_COLOR,
            font=tkfont.Font(family=SHARED_FONT_CUSTOM, size=18, weight="bold"),
            anchor="w",
        )
        lbl.grid(row=0, column=0, sticky="ew", padx=8)

        # Make it span full width of the grid area
        row.grid(columnspan=cols, sticky="ew", padx=0, pady=(10, 6))
        return row
    def _current_open_collection_name(self) -> str | None:
        payload = getattr(self, "page_payload", {}) or {}
        name = payload.get("name")
        return (name or "").strip() or None
    def _delete_collection_by_name(self, name: str) -> bool:
        """
        Best-effort delete:
        1) If LibraryData exposes a delete method, use it.
        2) Otherwise, show a clear error so you can add a delete method to LibraryData.
        """
        name = (name or "").strip()
        if not name:
            return False

        cid = None
        try:
            cid = self.data._find_collection_id_by_name(name)  # defined in LibraryData
        except Exception:
            cid = None

        if not cid:
            return False

        try:
            return bool(self.data.delete_collection(cid, persist=True))
        except Exception:
            return False
    def _side_edit_collections(self):
        rows = self._collections_all()
        names = [(r.get("name") or "").strip() for r in rows]
        names = [n for n in names if n]

        if not names:
            messagebox.showinfo("Edit Collections", "No collections to edit yet.")
            return

        win = tk.Toplevel(self)
        win.title("Edit Collections")
        win.transient(self)
        win.grab_set()

        # Match your app styling
        win.configure(bg=EDITCOLL_BG_COLOR if "PANEL_BG" in globals() else THEME_COLOR2)
        win.geometry("640x520")

        # --- top title ---
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=34, weight="bold")
        sub_font = tkfont.Font(family=SHARED_FONT_TABLE, size=14)
        btn_font = tkfont.Font(family=SHARED_FONT_BUTTON, size=18)

        header = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        header.pack(fill="x", padx=22, pady=(18, 8))

        tk.Label(
            header,
            text="Edit Collections",
            bg=win["bg"],
            fg=EDITCOLL_HEADER_TEXT_COLOR,
            font=title_font
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Select one or more collections, then delete. (Hold ⌘/Ctrl or Shift for multiple.)",
            bg=win["bg"],
            fg=SHARED_ALPHA_MUTED_TEXT_COLOR,
            font=sub_font
        ).pack(anchor="w", pady=(6, 0))

        # --- list area ---
        body = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        body.pack(fill="both", expand=True, padx=22, pady=(10, 12))

        lb_frame = tk.Frame(body, bg=win["bg"], highlightthickness=0, bd=0)
        lb_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(lb_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        lb = tk.Listbox(
            lb_frame,
            selectmode="extended",
            yscrollcommand=scrollbar.set,
            activestyle="none",
            font=tkfont.Font(family=SHARED_FONT_TABLE, size=18),
            bd=0,
            highlightthickness=1,
            relief="flat",
            exportselection=False,
        )
        scrollbar.config(command=lb.yview)
        lb.pack(side="left", fill="both", expand=True)

        for n in sorted(names, key=lambda s: s.lower()):
            lb.insert("end", n)

        # --- footer controls ---
        footer = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        footer.pack(fill="x", padx=22, pady=(0, 18))

        count_var = tk.StringVar(value="0 selected")

        def _update_count(*_):
            count_var.set(f"{len(lb.curselection())} selected")

        lb.bind("<<ListboxSelect>>", _update_count)
        tk.Label(footer, textvariable=count_var, bg=win["bg"], fg=BOOKDETAIL_TAGHOLDER_BG_COLOR, font=sub_font).pack(anchor="w")

        btn_row = tk.Frame(footer, bg=win["bg"], highlightthickness=0, bd=0)
        btn_row.pack(fill="x", pady=(10, 0))

        def do_delete_selected():
            idxs = list(lb.curselection())
            if not idxs:
                messagebox.showwarning("Delete", "Select at least one collection.")
                return

            selected = [lb.get(i) for i in idxs]
            preview = "\n".join(f"• {n}" for n in selected[:10])
            if len(selected) > 10:
                preview += f"\n… (+{len(selected) - 10} more)"

            ok = messagebox.askyesno(
                "Confirm delete",
                "Delete these collections?\n\n"
                f"{preview}\n\n"
                "This cannot be undone."
            )
            if not ok:
                return

            deleted_any = False
            for name in selected:
                deleted_any = self._delete_collection_by_name(name) or deleted_any

            if deleted_any:
                try:
                    win.destroy()
                except Exception:
                    pass
                self.show_collections_page()
            else:
                messagebox.showerror("Delete failed", "No collections were deleted.")

        def close():
            try:
                win.destroy()
            except Exception:
                pass

        del_btn = tk.Button(
            btn_row,
            text="Delete Selected",
            command=do_delete_selected,
            bg=EDITCOLL_BTN_TEXT_COLOR,
            fg=EDITCOLL_BTN_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            bd=0,
            highlightthickness=0,
            font=btn_font,
            padx=18,
            pady=10,
        )
        del_btn.pack(side="left")

        cancel_btn = tk.Button(
            btn_row,
            text="Cancel",
            command=close,
            bg=EDITCOLL_BTN_TEXT_COLOR,
            fg=EDITCOLL_BTN_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            bd=0,
            highlightthickness=0,
            font=btn_font,
            padx=18,
            pady=10,
        )
        cancel_btn.pack(side="right")
    def _side_edit_open_collection(self):
        name = self._current_open_collection_name()
        if not name:
            messagebox.showerror("Edit Collection", "No collection is currently open.")
            return
        rec = self._get_collection_record(name) or self._find_collection_record(name)
        if not rec:
            messagebox.showerror("Edit Collection", f'Collection "{name}" was not found.')
            return
        ids = list(self._collection_book_ids(rec))
        # Pass the collection_id so we can properly update (rename) instead of creating duplicate
        cid = rec.get("collection_id") or ""
        self.show_build_collection_page(prefill_name=name, prefill_ids=ids, edit_collection_id=cid)
    def _side_duplicate_collection(self):
        """Duplicate the currently-shown build-collection into a new saved collection, then open it."""
        # We duplicate from the Build Collection page state (name var + selected ids).
        name_var = getattr(self, "_build_collection_name_var", None)
        src_name = (name_var.get() if name_var is not None else "") or ""
        src_name = src_name.strip()
        if not src_name:
            src_name = "Untitled Collection"

        src_ids = list(getattr(self, "_build_collection_selected", []) or [])

        # Find an available copy name: "Name 2", then 3, 4, ...
        existing = {((c.get("name") or "").strip().lower()) for c in (self._collections_all() or [])}
        base = src_name
        n = 2
        while True:
            candidate = f"{base} {n}"
            if candidate.strip().lower() not in existing:
                new_name = candidate
                break
            n += 1

        # ✅ Save immediately to disk (persist across sessions) BEFORE switching pages
        try:
            self.data.upsert_collection(new_name, src_ids, persist=True)
        except Exception as e:
            messagebox.showerror("Duplicate failed", str(e))
            return

        # Open build page for the copy (so user can edit further)
        self.show_build_collection_page(prefill_name=new_name, prefill_ids=src_ids)
    def _side_toggle_mark_as_read(self):
        # Toggle mode
        self._mark_read_mode = not getattr(self, "_mark_read_mode", False)

        # Force list view when enabling mark-read mode (checkboxes only appear in list view)
        if self._mark_read_mode:
            self._mark_read_force_list = True
        else:
            self._mark_read_force_list = False

        # Rebuild the current page so the list column appears/disappears cleanly
        name = self._current_open_collection_name()
        if name:
            self.show_open_collection_page(name)
    def _side_add_to_collection(self):
        """Show popup to add the current book to a collection."""
        book = getattr(self, "_current_book_detail", None) or (getattr(self, "page_payload", {}) or {}).get("book")
        if not isinstance(book, dict) or not book:
            messagebox.showerror("Add to Collection", "No book is currently displayed.")
            return

        bid = (book.get("book_id") or "").strip()
        if not bid:
            messagebox.showerror("Add to Collection", "This book has no book_id.")
            return

        book_title = self._unescape_entities(book.get("title") or "Untitled").strip()


        # Get all collections
        collections = self._collections_all()
        if not collections:
            messagebox.showinfo("Add to Collection", "No collections exist yet. Create one first from the Collections page.")
            return

        # Create popup window
        win = tk.Toplevel(self)
        win.title("Add to Collection")
        win.transient(self)
        win.grab_set()
        win.configure(bg=EDITCOLL_BG_COLOR if "EDITCOLL_BG" in globals() else THEME_COLOR2)
        win.geometry("550x480")

        # Center on parent
        win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 550) // 2
        y = self.winfo_y() + (self.winfo_height() - 480) // 2
        win.geometry(f"+{x}+{y}")

        # Fonts
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=28, weight="bold")
        sub_font = tkfont.Font(family=SHARED_FONT_TABLE, size=14)
        btn_font = tkfont.Font(family=SHARED_FONT_BUTTON, size=16)
        list_font = tkfont.Font(family=SHARED_FONT_TABLE, size=16)

        # Header
        header = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            header,
            text="Add to Collection",
            bg=win["bg"],
            fg=EDITCOLL_HEADER_TEXT_COLOR,
            font=title_font
        ).pack(anchor="w")

        # Book title being added
        tk.Label(
            header,
            text=f'Adding: "{self._ellipsize_px(book_title, sub_font, 450)}"',
            bg=win["bg"],
            fg=EDITCOLL_SUBTEXT_COLOR if "COLL_POP_SUBTEXT" in globals() else "gray",
            font=sub_font
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            header,
            text="Select a collection:",
            bg=win["bg"],
            fg=EDITCOLL_HEADER_TEXT_COLOR,
            font=sub_font
        ).pack(anchor="w", pady=(10, 0))

        # List area
        body = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        body.pack(fill="both", expand=True, padx=20, pady=(8, 10))

        lb_frame = tk.Frame(body, bg=win["bg"], highlightthickness=0, bd=0)
        lb_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(lb_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        lb = tk.Listbox(
            lb_frame,
            selectmode="single",
            yscrollcommand=scrollbar.set,
            activestyle="none",
            font=list_font,
            bd=0,
            highlightthickness=1,
            relief="flat",
            exportselection=False,
        )
        scrollbar.config(command=lb.yview)
        lb.pack(side="left", fill="both", expand=True)

        # Sort collections by name and populate
        sorted_collections = sorted(collections, key=lambda c: (c.get("name") or "").lower())
        for col in sorted_collections:
            name = (col.get("name") or "").strip()
            if name:
                count = len(col.get("book_ids") or [])
                lb.insert("end", f"{name}  ({count} books)")

        # Store mapping of display text to collection name
        collection_names = [((c.get("name") or "").strip()) for c in sorted_collections if (c.get("name") or "").strip()]

        # Footer with buttons
        footer = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        footer.pack(fill="x", padx=20, pady=(0, 16))

        btn_row = tk.Frame(footer, bg=win["bg"], highlightthickness=0, bd=0)
        btn_row.pack(fill="x")

        def do_save():
            sel = lb.curselection()
            if not sel:
                messagebox.showwarning("Add to Collection", "Please select a collection.", parent=win)
                return

            idx = sel[0]
            if idx >= len(collection_names):
                return

            col_name = collection_names[idx]

            # Check if book is already in collection
            col_rec = self._find_collection_record(col_name)
            if col_rec:
                existing_ids = self._collection_book_ids(col_rec)
                if bid in existing_ids:
                    messagebox.showinfo("Already Added", f'"{book_title}" is already in "{col_name}".', parent=win)
                    return

            # Add book to collection
            try:
                success = self.data.add_book_to_collection(col_name, bid, persist=True)
                if success:
                    messagebox.showinfo("Success", f'Added "{book_title}" to "{col_name}".', parent=win)
                    win.destroy()
                else:
                    messagebox.showerror("Failed", f'Could not add book to "{col_name}".', parent=win)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)

        def do_cancel():
            win.destroy()

        def do_preview():
            sel = lb.curselection()
            if not sel:
                messagebox.showwarning("Preview Collection", "Please select a collection to preview.", parent=win)
                return

            idx = sel[0]
            if idx >= len(collection_names):
                return

            col_name = collection_names[idx]
            self._show_collection_preview_popup(col_name, parent=win)

        # Preview button (left)
        preview_btn = tk.Button(
            btn_row,
            text="Preview Collection",
            command=do_preview,
            bg=SHARED_BUTTON1_BG_COLOR,
            fg=SHARED_BUTTON1_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            bd=0,
            highlightthickness=0,
            font=btn_font,
            padx=14,
            pady=8,
            cursor="hand2",
        )
        preview_btn.pack(side="left")

        # Cancel button (right)
        cancel_btn = tk.Button(
            btn_row,
            text="Cancel",
            command=do_cancel,
            bg=SHARED_BUTTON1_BG_COLOR,
            fg=SHARED_BUTTON1_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            bd=0,
            highlightthickness=0,
            font=btn_font,
            padx=14,
            pady=8,
            cursor="hand2",
        )
        cancel_btn.pack(side="right")

        # Save button (right, next to cancel)
        save_btn = tk.Button(
            btn_row,
            text="Add to Collection",
            command=do_save,
            bg=SHARED_BUTTON1_BG_COLOR,
            fg=SHARED_BUTTON1_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            bd=0,
            highlightthickness=0,
            font=btn_font,
            padx=14,
            pady=8,
            cursor="hand2",
        )
        save_btn.pack(side="right", padx=(0, 10))
    def _show_collection_preview_popup(self, collection_name: str, parent=None):
        """Show a preview popup with collection books, authors, and top tags."""
        col_rec = self._find_collection_record(collection_name)
        if not col_rec:
            messagebox.showerror("Preview", f'Collection "{collection_name}" not found.', parent=parent)
            return

        book_ids = self._collection_book_ids(col_rec)
        books = self._books_by_ids(book_ids)

        # Create popup
        win = tk.Toplevel(parent or self)
        win.title(f"Preview: {collection_name}")
        win.transient(parent or self)
        win.grab_set()
        win.configure(bg=EDITCOLL_BG_COLOR if "EDITCOLL_BG" in globals() else THEME_COLOR2)
        win.geometry("600x550")

        # Center on parent
        win.update_idletasks()
        px = (parent or self).winfo_x()
        py = (parent or self).winfo_y()
        pw = (parent or self).winfo_width()
        ph = (parent or self).winfo_height()
        x = px + (pw - 600) // 2
        y = py + (ph - 550) // 2
        win.geometry(f"+{x}+{y}")

        # Fonts
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=26, weight="bold")
        tag_font = tkfont.Font(family=SHARED_FONT_TABLE, size=12)
        sub_font = tkfont.Font(family=SHARED_FONT_TABLE, size=13)
        list_font = tkfont.Font(family=SHARED_FONT_TABLE, size=14)
        btn_font = tkfont.Font(family=SHARED_FONT_BUTTON, size=16)

        # Header
        header = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        header.pack(fill="x", padx=20, pady=(16, 6))

        tk.Label(
            header,
            text=collection_name,
            bg=win["bg"],
            fg=EDITCOLL_HEADER_TEXT_COLOR,
            font=title_font
        ).pack(anchor="w")

        tk.Label(
            header,
            text=f"{len(books)} book{'s' if len(books) != 1 else ''}",
            bg=win["bg"],
            fg=EDITCOLL_SUBTEXT_COLOR if "COLL_POP_SUBTEXT" in globals() else "gray",
            font=sub_font
        ).pack(anchor="w", pady=(2, 0))

        # Get top tags using data layer
        top_tags = self.data.top_tags_for_books(book_ids, limit=8)

        # Display tags if any
        if top_tags:
            tags_frame = tk.Frame(header, bg=win["bg"], highlightthickness=0, bd=0)
            tags_frame.pack(anchor="w", pady=(8, 0))

            tk.Label(
                tags_frame,
                text="Top Tags:",
                bg=win["bg"],
                fg=EDITCOLL_HEADER_TEXT_COLOR,
                font=sub_font
            ).pack(side="left", padx=(0, 8))

            # Create tag chips
            chips_frame = tk.Frame(tags_frame, bg=win["bg"], highlightthickness=0, bd=0)
            chips_frame.pack(side="left")

            for tag in top_tags:
                chip = tk.Label(
                    chips_frame,
                    text=tag.title(),
                    bg=BOOKDETAIL_TAGDISPLAY_BG_COLOR,
                    fg=BOOKDETAIL_TAGDISPLAY_TEXT_COLOR,
                    font=tag_font,
                    padx=8,
                    pady=2,
                )
                chip.pack(side="left", padx=2, pady=2)

        # Books list area
        body = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        body.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # Column headers
        header_row = tk.Frame(body, bg=SHARED_SUBHEADER_BG_COLOR if "SUB_HEADER_BG" in globals() else "#ddd", highlightthickness=0, bd=0)
        header_row.pack(fill="x")

        tk.Label(
            header_row,
            text="Title",
            bg=SHARED_SUBHEADER_BG_COLOR if "SUB_HEADER_BG" in globals() else "#ddd",
            fg=SHARED_SUBHEADER_TEXT_COLOR if "SUB_HEADER_TEXT" in globals() else "#333",
            font=(SHARED_FONT_TABLE, 13, "bold"),
            anchor="w",
            padx=10,
            pady=6,
            width=30,
        ).pack(side="left", fill="x", expand=True)

        tk.Label(
            header_row,
            text="Author",
            bg=SHARED_SUBHEADER_BG_COLOR if "SUB_HEADER_BG" in globals() else "#ddd",
            fg=SHARED_SUBHEADER_TEXT_COLOR if "SUB_HEADER_TEXT" in globals() else "#333",
            font=(SHARED_FONT_TABLE, 13, "bold"),
            anchor="w",
            padx=10,
            pady=6,
            width=25,
        ).pack(side="left", fill="x", expand=True)

        # Scrollable list
        list_frame = tk.Frame(body, bg=win["bg"], highlightthickness=0, bd=0)
        list_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(list_frame, bg=win["bg"], highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scroll_inner = tk.Frame(canvas, bg=win["bg"])

        scroll_inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # Populate book list
        if not books:
            tk.Label(
                scroll_inner,
                text="No books in this collection.",
                bg=win["bg"],
                fg=EDITCOLL_SUBTEXT_COLOR if "COLL_POP_SUBTEXT" in globals() else "gray",
                font=list_font,
                pady=20,
            ).pack()
        else:
            for idx, b in enumerate(books):
                row_bg = SHARED_TABLE_ALTROW_BG_COLOR if idx % 2 == 0 else SHARED_TABLE_BG_COLOR

                row = tk.Frame(scroll_inner, bg=row_bg, highlightthickness=0, bd=0)
                row.pack(fill="x")

                title = self._unescape_entities(b.get("title") or "Untitled").strip()
                first = (b.get("first_name") or "").strip()
                last = (b.get("last_name") or "").strip()
                creators = (b.get("creators") or "").strip()
                author = f"{first} {last}".strip() if (first or last) else (creators or "Unknown")

                # Truncate long text
                title_display = title if len(title) <= 40 else title[:37] + "..."
                author_display = author if len(author) <= 30 else author[:27] + "..."

                tk.Label(
                    row,
                    text=title_display,
                    bg=row_bg,
                    fg=SHARED_SCROLLROW_TEXT_COLOR,
                    font=list_font,
                    anchor="w",
                    padx=10,
                    pady=6,
                    width=35,
                ).pack(side="left", fill="x", expand=True)

                tk.Label(
                    row,
                    text=author_display,
                    bg=row_bg,
                    fg=SHARED_SCROLLROW_TEXT_COLOR,
                    font=list_font,
                    anchor="w",
                    padx=10,
                    pady=6,
                    width=28,
                ).pack(side="left", fill="x", expand=True)

        # Close button
        footer = tk.Frame(win, bg=win["bg"], highlightthickness=0, bd=0)
        footer.pack(fill="x", padx=20, pady=(0, 16))

        close_btn = tk.Button(
            footer,
            text="Close",
            command=win.destroy,
            bg=SHARED_BUTTON1_BG_COLOR,
            fg=SHARED_BUTTON1_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            bd=0,
            highlightthickness=0,
            font=btn_font,
            padx=20,
            pady=8,
            cursor="hand2",
        )
        close_btn.pack(side="right")
    def _show_customize_genres_popup(self):
        """Show a popup to add/edit/delete genres."""
        # Store current tab BEFORE creating popup (page_payload may change)
        current_tab = getattr(self, "page_payload", {}).get("tab", "fiction") if hasattr(self, "page_payload") else "fiction"

        popup = tk.Toplevel(self)
        popup.title("Customize Genres")
        popup.transient(self)
        popup.grab_set()

        # Center popup on main window
        popup_w, popup_h = 450, 550
        x = self.winfo_x() + (self.winfo_width() - popup_w) // 2
        y = self.winfo_y() + (self.winfo_height() - popup_h) // 2
        popup.configure(bg=GENRESPOP_MAIN_BG_COLOR)
        popup.geometry(f"{popup_w}x{popup_h}+{x}+{y}")
        popup.resizable(False, False)

        # Header
        header_frame = tk.Frame(popup, bg=GENRESPOP_HEADER_BG_COLOR, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Customize Genres",
            bg=GENRESPOP_HEADER_BG_COLOR,
            fg=GENRESPOP_HEADER_TEXT_COLOR,
            font=(SHARED_FONT_CUSTOM, 22, "bold"),
        ).pack(pady=12)

        # Instructions
        tk.Label(
            popup,
            text="Add, edit, or remove genres. Click × to mark for deletion.",
            font=(SHARED_FONT_CUSTOM, 18),
            bg=GENRESPOP_MAIN_BG_COLOR,
            fg=GENRESPOP_SUBTEXT_COLOR,
            justify="center",
        ).pack(pady=(10, 5))

        # Add genre entry bar
        def add_new_genre(event=None):
            """Add a new genre from the entry bar."""
            new_name = add_entry.get().strip().title()
            if not new_name:
                return

            # Check if already exists
            existing = get_all_current_genres()
            # Also check pending new genres
            for orig, changes in pending_changes.items():
                if changes.get("is_new") and not changes.get("deleted"):
                    existing.append(changes.get("new_name", orig))

            if new_name in existing:
                messagebox.showwarning("Genre Exists", f'"{new_name}" already exists.', parent=popup)
                return

            # Add to pending changes as a new genre
            pending_changes[new_name] = {"new_name": new_name, "deleted": False, "is_new": True}

            # Clear entry and refresh
            add_entry.delete(0, tk.END)
            render_genre_list()

        add_frame = tk.Frame(popup, bg=GENRESPOP_MAIN_BG_COLOR)
        add_frame.pack(fill="x", padx=15, pady=(5, 5))

        add_entry = tk.Entry(
            add_frame,
            font=(SHARED_FONT_CUSTOM, 18),
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightcolor=SHARED_ENTRY1_BORDER_COLOR,
        )
        add_entry.pack(side="right", fill="x", expand=True, padx=(0, 8), ipady=6)
        add_entry.configure(bg=SHARED_ENTRY1_BG_COLOR, fg=SHARED_ENTRY1_TEXT_COLOR)

        wrap, add_btn = self._make_square_icon_btn(
            add_frame,
            text="+",
            cmd=add_new_genre,
            size_px=38,
            bg=GENRESPOP_ADDBTN_BG_COLOR,
            fg=GENRESPOP_ADDBTN_TEXT_COLOR,
            font_tuple=(SHARED_FONT_CUSTOM, 34, "bold"),
        )
        add_btn.configure(highlightthickness=1, highlightcolor=SHARED_ENTRY1_BORDER_COLOR, anchor="center", justify="center", padx=0, pady=0)
        wrap.pack(side="right", padx=(0, 0), pady=0,)

        # List frame with scrollbar
        list_container = tk.Frame(popup, bg=GENRESPOP_LIST_BORDER_COLOR, bd=1, relief="sunken")
        list_container.pack(fill="both", expand=True, padx=20, pady=5)

        canvas = tk.Canvas(list_container, bg=GENRESPOP_LIST_BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=THEME_COLOR2)

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        pending_changes: dict[str, dict] = {}
        genre_widgets: dict[str, dict] = {}

        def get_all_current_genres() -> list[str]:
            """Get all genres (standard + custom) with overrides applied."""
            genres = []

            # Standard genres (with any existing renames applied)
            for g in self.data.FICTION_GENRES + self.data.NONFICTION_GENRES:
                if hasattr(self.data, 'is_genre_deleted') and self.data.is_genre_deleted(g):
                    continue
                effective = self.data.get_effective_genre_name(g) if hasattr(self.data, 'get_effective_genre_name') else g
                if effective not in genres:
                    genres.append(effective)

            # Custom genres
            user_genres = self.data.get_user_genres() if hasattr(self.data, 'get_user_genres') else []
            for g in user_genres:
                if g not in genres:
                    genres.append(g)

            return sorted(genres, key=str.lower)

        def render_genre_list():
            """Render the genre list."""
            for widget in scrollable.winfo_children():
                widget.destroy()
            genre_widgets.clear()

            # Get base genres and apply pending changes
            base_genres = get_all_current_genres()

            # Add any new genres from pending_changes
            for orig, changes in pending_changes.items():
                if changes.get("is_new") and not changes.get("deleted"):
                    display_name = changes.get("new_name", orig)
                    if display_name not in base_genres:
                        base_genres.append(display_name)

            # Sort alphabetically
            display_genres = []
            for g in base_genres:
                # Check if this genre has pending changes
                pending = None
                for orig, changes in pending_changes.items():
                    current_name = changes.get("new_name", orig)
                    if current_name == g or orig == g:
                        pending = (orig, changes)
                        break

                if pending:
                    orig, changes = pending
                    if not changes.get("deleted"):
                        display_genres.append((orig, changes.get("new_name", orig), changes.get("deleted", False)))
                else:
                    display_genres.append((g, g, False))

            # Sort by display name
            display_genres.sort(key=lambda x: x[1].lower())

            for original_name, display_name, is_deleted in display_genres:
                row = tk.Frame(scrollable, bg=THEME_COLOR2 if not is_deleted else GENRESPOP_ROW_DISABLED_BG_COLOR)
                row.pack(fill="x", pady=1, padx=5)

                # Delete/restore button (×)
                bg_idle = GENRESPOP_ADDBTN_BG_COLOR  # pick your “square button bg”
                fg_idle = SHARED_XBTN_IDLE_COLOR
                bg_deleted = GENRESPOP_ROW_DISABLED_BG_COLOR  # or whatever you want when deleted
                fg_deleted = SHARED_XBTN_SELECTED_BG_COLOR

                def toggle_delete(orig=original_name):
                    """Toggle deletion state for a genre."""
                    if orig not in pending_changes:
                        pending_changes[orig] = {"new_name": orig, "deleted": False, "is_new": False}

                    pending_changes[orig]["deleted"] = not pending_changes[orig]["deleted"]
                    is_del = pending_changes[orig]["deleted"]

                    widgets = genre_widgets.get(orig)
                    if not widgets:
                        return

                    # Update row + entry
                    widgets["row"].configure(bg=GENRESPOP_ROW_DISABLED_BG_COLOR if is_del else THEME_COLOR2)
                    widgets["name_entry"].configure(
                        bg=GENRESPOP_LIST_BG_COLOR if not is_del else GENRESPOP_ROW_DISABLED_BG_COLOR,
                        fg=GENRESPOP_LIST_TEXT_COLOR if not is_del else GENRESPOP_SUBTEXT_COLOR,
                        state="disabled" if is_del else "normal",
                    )

                    # Update BOTH wrapper + button so the square stays clean
                    new_bg = bg_deleted if is_del else bg_idle
                    new_fg = fg_deleted if is_del else fg_idle
                    widgets["wrap"].configure(bg=new_bg)
                    widgets["del_btn"].configure(bg=new_bg, fg=new_fg, activebackground=new_bg, activeforeground=new_fg)

                wrap, del_btn = self._make_square_icon_btn(
                    row,
                    text="×",
                    cmd=toggle_delete,  # ✅ no extra parens, and no later configure needed
                    size_px=34,
                    bg=(bg_deleted if is_deleted else bg_idle),
                    fg=(fg_deleted if is_deleted else fg_idle),
                    font_tuple=(SHARED_FONT_CUSTOM, 14),
                )

                # Add square border like your + button
                wrap.configure(highlightthickness=1, highlightbackground="black")
                wrap.pack(side="left", padx=(2, 8), pady=4)

                # Editable genre name entry
                name_var = tk.StringVar(value=display_name)
                name_entry = tk.Entry(
                    row,
                    textvariable=name_var,
                    font=(SHARED_FONT_CUSTOM, 20),
                    bg=GENRESPOP_LIST_BG_COLOR if not is_deleted else SHARED_ALPHA_MUTED_TEXT_COLOR,
                    fg=GENRESPOP_LIST_TEXT_COLOR if not is_deleted else SHARED_ALPHA_MUTED_TEXT_COLOR,
                    bd=0,
                    highlightthickness=0,
                    state="normal" if not is_deleted else "disabled",
                )
                name_entry.pack(side="left", fill="x", expand=True, pady=4, padx=(0, 5))

                # Store reference for updates
                genre_widgets[original_name] = {
                    "row": row,
                    "wrap": wrap,
                    "del_btn": del_btn,
                    "name_var": name_var,
                    "name_entry": name_entry,
                    "is_deleted": is_deleted,
                }

                def on_name_change(event=None, orig=original_name, var=name_var):
                    """Track name changes."""
                    new_name = var.get().strip()
                    if orig not in pending_changes:
                        pending_changes[orig] = {"new_name": orig, "deleted": False, "is_new": False}
                    pending_changes[orig]["new_name"] = new_name if new_name else orig


                name_entry.bind("<FocusOut>", lambda e, o=original_name, v=name_var: on_name_change(e, o, v))
                name_entry.bind("<Return>", lambda e, o=original_name, v=name_var: on_name_change(e, o, v))


        def save_changes():
            """Save all pending changes."""
            changes_made = False
            books_updated = 0

            for original_name, changes in pending_changes.items():
                new_name = changes.get("new_name", original_name).strip().title()
                is_deleted = changes.get("deleted", False)
                is_new = changes.get("is_new", False)

                if is_new:
                    if not is_deleted and new_name:
                        # Add new genre
                        self.data.add_user_genre(new_name)
                        changes_made = True
                else:
                    if is_deleted:
                        # Delete the genre - data layer now handles clearing from books
                        count = self.data.delete_genre(original_name)
                        books_updated += count
                        changes_made = True
                    elif new_name != original_name and new_name:
                        # Rename the genre
                        count = self.data.rename_genre(original_name, new_name)
                        books_updated += count
                        changes_made = True

            if changes_made:
                self.data.save()
                self._refresh_catalog_from_data()

            popup.destroy()

        def cancel_changes():
            """Close without saving."""
            popup.destroy()

        # Bind add button and entry
        add_btn.configure(command=add_new_genre)
        add_entry.bind("<Return>", add_new_genre)

        # Button frame
        btn_frame = tk.Frame(popup)
        btn_frame.pack(fill="x", pady=10, padx=20)
        btn_frame.configure(bg=GENRESPOP_MAIN_BG_COLOR)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=cancel_changes,
            bg=GENRESPOP_BTN_BG_COLOR,
            fg=GENRESPOP_BTN_TEXT_COLOR,
            font=(SHARED_FONT_CUSTOM, 12),
            bd=0,
            relief="solid",
            padx=15,
            pady=8,
            cursor="hand2",
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="Save",
            command=save_changes,
            bg=BROWSEGENRES_PANEL_BG_COLOR,
            fg=GENRESPOP_BTN_TEXT_COLOR,
            font=(SHARED_FONT_CUSTOM, 12),
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
        ).pack(side="right")

        # Initial render
        render_genre_list()

        # Focus on entry
        add_entry.focus_set()

        # Make popup modal
        popup.wait_window()

        # Refresh the browse genres page after closing (use stored tab from before popup)
        self.show_browse_genres_page(current_tab)

    # ---------- FONTS ----------
    def _init_fonts(self):
        import tkinter.font as tkfont

        def pick(preferred, fallbacks):
            fams = set(tkfont.families())
            for name in [preferred, *fallbacks]:
                if name in fams:
                    return name
            return fallbacks[-1] if fallbacks else "Segoe UI"

        global SHARED_FONT_CUSTOM, SHARED_FONT_BUTTON, SHARED_FONT_TABLE
        global SHARED_TABLE_HEADER_FONT, SHARED_TABLE_ROW_FONT
        global ENTRY_BAR_FONT_FAMILY

        SHARED_FONT_TABLE = pick("Liberation Sans", ["Cambria", "Segoe UI", "Calibri", "Arial"])
        SHARED_FONT_CUSTOM = pick("AESTHICA", ["Lucida Handwriting", "Segoe Script", "Georgia"])
        SHARED_FONT_BUTTON = pick("Sherly Kitchen", ["Garamond", "Georgia", "Cambria", "Times New Roman"])

        ENTRY_BAR_FONT_FAMILY = SHARED_FONT_CUSTOM
        SHARED_TABLE_HEADER_FONT = (SHARED_FONT_TABLE, 20, "bold")
        SHARED_TABLE_ROW_FONT = (SHARED_FONT_TABLE, 18)

        self.title_font = tkfont.Font(
            family=SHARED_FONT_CUSTOM, size=82, weight="bold"
        )
        self.subtitle_font = tkfont.Font(
            family=SHARED_FONT_CUSTOM, size=32
        )
        self.button_font = tkfont.Font(
            family=SHARED_FONT_BUTTON, size=28
        )
        self.genre_font = tkfont.Font(
            family=SHARED_FONT_BUTTON, size=22
        )
        self.left_button_font = tkfont.Font(
            family=SHARED_FONT_BUTTON, size=22
        )

    # ---------- BACKGROUND / UI HELPERS ----------
    def _load_background_image(self):
        if not BG_IMAGE_PATH.exists():
            raise FileNotFoundError(f"Background image not found at: {BG_IMAGE_PATH}")
        # keep an original source image; never resize this in-place
        self._bg_pil = Image.open(BG_IMAGE_PATH)
        self._update_background_image()
    def _update_background_image(self):
        """Cover-fit background: fills window without distortion, center-crops overflow."""
        if self._bg_pil is None:
            return

        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 1 or height <= 1:
            return

        # ✅ cover-fit + center crop
        fitted = ImageOps.fit(
            self._bg_pil,
            (width, height),
            method=Image.LANCZOS,
            centering=(0.5, 0.5),  # center crop
        )

        self._bg_tk = ImageTk.PhotoImage(fitted)

        self.canvas.delete("bg")
        self.canvas.create_image(0, 0, image=self._bg_tk, anchor="nw", tags="bg")
        self.canvas.tag_lower("bg")
    def set_background(self, image_path: Path):
        if not image_path.exists():
            raise FileNotFoundError(f"Background image not found: {image_path}")
        # keep an original source image; never resize this in-place
        self._bg_pil = Image.open(image_path)
        self._update_background_image()
    def _ui_font(self, family: str, size: int, weight: str | None = None, slant: str | None = None):
        kw = {"family": family, "size": size}
        if weight: kw["weight"] = weight
        if slant: kw["slant"] = slant
        return tkfont.Font(**kw)
    def _make_square_icon_btn(self, parent, *, text, cmd, size_px: int, bg: str, fg: str, font_tuple):
        """Square icon button (perfect square via wrapper frame)."""
        wrap = tk.Frame(parent, width=size_px, height=size_px, bg=bg, highlightthickness=0, bd=0)
        wrap.pack_propagate(False)

        btn = tk.Button(
            wrap,
            text=text,
            command=cmd,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            bd=0,
            highlightthickness=0,
            relief="flat",
            takefocus=False,
            font=font_tuple,
            padx=0,
            pady=0,
        )
        btn.pack(fill="both", expand=True)

        self.active_widgets.extend([wrap, btn])
        return wrap, btn
    def _style_entry(self, entry: tk.Entry):
        """Consistent entry styling that matches your UI."""
        entry.config(
            bg=SHARED_ALPHA_MUTED_TEXT_COLOR,
            fg=SHARED_ALPHA_MUTED_TEXT_COLOR,
            insertbackground=SHARED_ALPHA_MUTED_TEXT_COLOR,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=FOCUS_PANEL_ACCENT_COLOR,
            highlightcolor=SHARED_ALPHA_MUTED_TEXT_COLOR,
        )
    def _on_escape_key(self, event=None):
        """Global Escape handler:
        - If side menu is open, close it
        - Otherwise, exit fullscreen/zoomed
        """
        if getattr(self, "_side_menu_open", False):
            self.close_side_menu()
            return "break"
        return self._escape_exit_fullscreen(event)

    # ---------- REUSABLE UI COMPONENT HELPERS ----------

    def _make_scrollable_listbox(self,parent: tk.Widget,*,selectmode: str = "single",font=None,
        bg: str | None = None,) -> tuple[tk.Frame, tk.Listbox, tk.Scrollbar]:
        """
        Create a scrollable listbox with consistent styling.
        
        Returns: (container_frame, listbox, scrollbar)
        """
        parent_bg = parent["bg"] if hasattr(parent, "__getitem__") else THEME_COLOR2
        lb_frame = tk.Frame(parent, bg=parent_bg, highlightthickness=0, bd=0)
        
        scrollbar = tk.Scrollbar(lb_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        lb = tk.Listbox(
            lb_frame,
            selectmode=selectmode,
            yscrollcommand=scrollbar.set,
            activestyle="none",
            font=font or tkfont.Font(family=SHARED_FONT_TABLE, size=18),
            bd=0,
            highlightthickness=1,
            relief="flat",
            exportselection=False,
            bg=bg,
        )
        scrollbar.config(command=lb.yview)
        lb.pack(side="left", fill="both", expand=True)
        
        self.active_widgets.extend([lb_frame, lb, scrollbar])
        return lb_frame, lb, scrollbar

    def _create_modal_popup(self,title: str,width: int = 500,height: int = 450,
        bg: str | None = None,parent: tk.Widget | None = None,) -> tuple[tk.Toplevel, tk.Frame, tk.Frame, tk.Frame]:
        """
        Create a standard modal popup with header, body, footer sections.
        
        Returns: (popup_window, header_frame, body_frame, footer_frame)
        """
        parent = parent or self
        bg = bg or EDITCOLL_BG_COLOR
        
        win = tk.Toplevel(parent)
        win.title(title)
        win.transient(parent)
        win.grab_set()
        win.configure(bg=bg)
        win.geometry(f"{width}x{height}")
        
        # Center on parent
        win.update_idletasks()
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - width) // 2
        y = py + (ph - height) // 2
        win.geometry(f"+{x}+{y}")
        
        # Create standard sections
        header = tk.Frame(win, bg=bg, highlightthickness=0, bd=0)
        header.pack(fill="x", padx=20, pady=(16, 8))
        
        body = tk.Frame(win, bg=bg, highlightthickness=0, bd=0)
        body.pack(fill="both", expand=True, padx=20, pady=(8, 10))
        
        footer = tk.Frame(win, bg=bg, highlightthickness=0, bd=0)
        footer.pack(fill="x", padx=20, pady=(0, 16))
        
        return win, header, body, footer

    # ---------- END REUSABLE UI COMPONENT HELPERS ----------

    def make_entry_bar(self,*,parent: tk.Widget,textvariable: tk.StringVar | None = None,font=None,) -> tuple[tk.Frame, tk.Entry]:

        frame = tk.Frame(parent, bg=SHARED_ENTRY1_BORDER_COLOR, highlightthickness=0, bd=0)

        frame.pack_propagate(False)

        entry = tk.Entry(
            frame,
            textvariable=textvariable,
            font=font or (SHARED_FONT_CUSTOM, 16),
            relief=SHARED_ENTRY_RELIEF_STYLE,
            bg=SHARED_ENTRY1_BG_COLOR,
            fg=SHARED_ENTRY1_TEXT_COLOR,
            insertbackground=SHARED_ENTRY_CURSOR_COLOR,
            justify=SHARED_ENTRY_JUSTIFY_STYLE,
            highlightthickness=0,
            bd=0,
        )
        entry.pack(fill="both", expand=True, padx=2, pady=2)


        return frame, entry

    # ---------- RESIZE / DESIGN PLACEMENT ----------
    def _is_fullscreen_like(self) -> bool:
        # 1) True fullscreen flag (works on many setups when you use attributes("-fullscreen", True))
        try:
            if bool(self.attributes("-fullscreen")):
                return True
        except tk.TclError:
            pass

        # 2) Zoomed/maximized (Windows often reports this)
        try:
            if self.state() == "zoomed":
                return True
        except tk.TclError:
            pass

        # 3) Fallback: window is ~screen size (macOS fullscreen often behaves like this)
        try:
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            ww = self.winfo_width()
            wh = self.winfo_height()
            return (ww >= sw - 10) and (wh >= sh - 80)
        except tk.TclError:
            return False
    def _on_resize(self, event):
        if event.widget is not self:
            return

        # debounce background + text + design widget reposition
        if self._resize_after_id is not None:
            try:
                self.after_cancel(self._resize_after_id)
            except tk.TclError:
                pass
        self._resize_after_id = self.after(80, self._handle_resize)

        # IMPORTANT: do NOT rebuild whole pages here.
        # Browse Genres will re-render its grid via its own debounced canvas <Configure>.
        # Settings doesn't need full rebuild either unless you have dynamic layout there.
    def _handle_resize(self):
        self._resize_after_id = None
        self._update_background_image()
        self._update_canvas_text_positions()
        self._reposition_design_widgets()
        self._refresh_menu_button_image()
        self._position_menu_button()
        self._position_left_nav_stack()

        if getattr(self, "current_page", "") == "build_collection":
            self._buildcol_relayout()

        if getattr(self, "_side_menu_open", False):
            self._position_side_menu_windows()
            self._refresh_side_menu_bg_image()
        if getattr(self, "current_page", "") == "book_detail":
            self._book_detail_relayout()
            self._book_detail_sync_genre_position()
            # keep book_detail canvas-pinned text items pinned on resize
            if getattr(self, "current_page", "") == "book_detail":
                for attr in ("_book_detail_genre", "_book_detail_tags"):
                    info = getattr(self, attr, None)
                    if not info:
                        continue

                    item = info.get("item")  # ✅ safe
                    if not item or not self.canvas.type(item):
                        continue

                    x_px, y_px = self._design_to_real_xy(info.get("x", 0), info.get("y", 0))
                    self.canvas.coords(item, x_px, y_px)

                    # tags needs wrap-width updates too
                    if attr == "_book_detail_tags":
                        try:
                            desired = int(info.get("wrap_w", 520))
                            right_pad = int(info.get("right_pad", 24))
                            max_fit = max(self.winfo_width() - x_px - right_pad, 120)
                            self.canvas.itemconfigure(item, width=max(120, min(desired, max_fit)))
                        except Exception:
                            pass
    def _apply_design_placement(self, widget: tk.Widget, design_x: int, design_y: int, anchor: str = "center"):
        win_w = max(self.winfo_width(), 1)
        win_h = max(self.winfo_height(), 1)

        offset_x = (win_w - SHARED_WINDOW_DESIGN_WIDTH) // 2
        offset_y = (win_h - SHARED_WINDOW_DESIGN_HEIGHT) // 2

        real_x = offset_x + design_x
        real_y = offset_y + design_y

        widget.place(x=real_x, y=real_y, anchor=anchor)
    def place_design(self, widget: tk.Widget, design_x: int, design_y: int, anchor: str = "center"):
        self._apply_design_placement(widget, design_x, design_y, anchor)
        self.placed_widgets.append((widget, design_x, design_y, anchor))
    def _reposition_design_widgets(self):
        for widget, dx, dy, anchor in list(self.placed_widgets):
            if not widget.winfo_exists():
                continue
            self._apply_design_placement(widget, dx, dy, anchor)
    def place_design_right_bias(self,widget: tk.Widget,design_x: int,design_y: int,anchor: str = "center",bias_ratio: float = 0.25):
        win_w = max(self.winfo_width(), 1)
        win_h = max(self.winfo_height(), 1)

        offset_x = (win_w - SHARED_WINDOW_DESIGN_WIDTH) // 2
        offset_y = (win_h - SHARED_WINDOW_DESIGN_HEIGHT) // 2

        extra_w = max(win_w - SHARED_WINDOW_DESIGN_WIDTH, 0)

        bias_x = int(extra_w * bias_ratio) if self._is_fullscreen_like() else 0

        widget.place(
            x=offset_x + design_x + bias_x,
            y=offset_y + design_y,
            anchor=anchor,
        )
    def _design_to_real_xy(self, design_x: int, design_y: int) -> tuple[int, int]:
        win_w = max(self.winfo_width(), 1)
        win_h = max(self.winfo_height(), 1)
        offset_x = (win_w - SHARED_WINDOW_DESIGN_WIDTH) // 2
        offset_y = (win_h - SHARED_WINDOW_DESIGN_HEIGHT) // 2
        return offset_x + design_x, offset_y + design_y
    def _update_design_placement_record(self, widget: tk.Widget, design_x: int, design_y: int, anchor: str = "center"):
        """
        Updates an already place_design()'d widget to a new design position.
        IMPORTANT: also updates self.placed_widgets so future resizes keep the new coords.
        """
        # Update the stored placement tuple
        for i, (w, dx, dy, a) in enumerate(list(self.placed_widgets)):
            if w is widget:
                self.placed_widgets[i] = (widget, design_x, design_y, anchor)
                break
        # Apply immediately
        self._apply_design_placement(widget, design_x, design_y, anchor)
    def _book_detail_sync_genre_position(self):
        """
        Recompute the genre canvas-text position from the CURRENT card geometry,
        then move the existing canvas item.
        This fixes fullscreen/resize not updating the genre Y.
        """
        info = getattr(self, "_book_detail_genre", None)
        if not info:
            return

        item = info.get("item")
        if not item or not self.canvas.type(item):
            return

        # Must exist (we store it when creating genre)
        genre_font = getattr(self, "_book_detail_genre_font", None)
        layout = getattr(self, "_book_detail_layout", None)
        if not genre_font or not layout:
            return

        # Pull latest card geometry (DESIGN units)
        CARD_X = int(layout["CARD_X"])
        CARD_Y = int(layout["CARD_Y"])
        CARD_W = int(layout["CARD_W"])
        CARD_H = int(layout["CARD_H"])
        pad_x = int(layout.get("pad_x", 20))

        card_left = CARD_X - (CARD_W // 2)
        card_top = CARD_Y - (CARD_H // 2)

        # Convert font height (PIXELS) -> DESIGN units so it scales correctly
        win_w = max(self.winfo_width(), 1)
        scale = max(0.85, min(1.45, win_w / 1280))
        genre_h_px = int(genre_font.metrics("linespace"))
        genre_h_design = int(round(genre_h_px / scale))

        GENRE_GAP = int(layout.get("GENRE_GAP", 10))
        genre_x_design = card_left + pad_x
        genre_y_design = card_top - genre_h_design - GENRE_GAP

        # Save + move
        info["x"], info["y"] = genre_x_design, genre_y_design
        x_px, y_px = self._design_to_real_xy(genre_x_design, genre_y_design)
        self.canvas.coords(item, x_px, y_px)

    # ---------- GLOBAL SCROLL ----------
    def _on_global_mousewheel(self, event):
        canvas = getattr(self, "_scroll_target", None)
        if not canvas or not canvas.winfo_exists():
            return

        # Figure out scroll direction across platforms:
        #   Windows/macOS: event.delta (positive = wheel up)
        #   Linux: Button-4 (up), Button-5 (down)
        step = None
        if getattr(event, "num", None) == 4:
            step = -1
        elif getattr(event, "num", None) == 5:
            step = 1
        else:
            delta = getattr(event, "delta", 0)
            if delta == 0:
                return
            step = -1 if delta > 0 else 1

        # Clamp: stop scrolling above the first row (top)
        y0, y1 = canvas.yview()  # fractions [0..1]
        if step < 0 and y0 <= 0.0:
            return "break"

        # (Optional but nice) Clamp bottom too, so no overscroll at the end
        if step > 0 and y1 >= 1.0:
            return "break"

        try:
            canvas.yview_scroll(step, "units")
        except tk.TclError:
            return

        return "break"
    def _register_scroll_canvas(self, canvas: tk.Canvas):
        canvas.bind("<Enter>", lambda e: setattr(self, "_scroll_target", canvas))
        canvas.bind("<Leave>", lambda e: setattr(self, "_scroll_target", None))

    # ---------- CANVAS TEXT ----------
    def make_canvas_text(self, text: str, relx: float, rely: float, font: tkfont.Font, fill:
    str = BACKGROUND_TITLE_TEXT, anchor: str = "center", justify: str = "left") -> int:
        width = max(self.winfo_width(), 1)
        height = max(self.winfo_height(), 1)

        x = relx * width
        y = rely * height

        item_id = self.canvas.create_text(
            x, y,
            text=text,
            fill=fill,
            font=font,
            anchor=anchor,
            justify=justify,
            tags=("ui_text",),  # ✅ renamed
        )
        self.canvas_text_items.append((item_id, relx, rely))
        return item_id
    def _update_canvas_text_positions(self):
        width = max(self.winfo_width(), 1)
        height = max(self.winfo_height(), 1)
        for item_id, relx, rely in self.canvas_text_items:
            x = relx * width
            y = rely * height
            self.canvas.coords(item_id, x, y)
    def clear_canvas_text(self):
        # remove ALL UI canvas text safely
        try:
            self.canvas.delete("ui_text")
        except Exception:
            pass

        for item_id, _, _ in self.canvas_text_items:
            try:
                self.canvas.delete(item_id)
            except Exception:
                pass
        self.canvas_text_items.clear()

    # ---------- WIDGET / BUTTON HELPERS ----------

    def _prompt_and_upload_cover(self, book_id: str, *, refresh_callback=None) -> bool:
        """
        Unified cover upload: prompts user, stores cover, persists.
        
        Args:
            book_id: The book to upload cover for
            refresh_callback: Optional callback to run after successful upload
            
        Returns:
            True if cover was uploaded successfully, False otherwise
        """
        bid = (book_id or "").strip()
        if not bid:
            return False

        path = filedialog.askopenfilename(
            title="Select Book Cover Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.gif"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("WEBP", "*.webp"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return False

        try:
            self.data.set_cover_from_file(bid, Path(path))
            self.data.save()
        except Exception as e:
            messagebox.showerror("Upload Cover", f"Could not set cover.\n\n{e}")
            return False

        # Refresh catalog cache
        try:
            self.catalog = list(self.data.catalog.values())
        except Exception:
            pass
        
        if refresh_callback:
            refresh_callback()
        
        return True
    def _upload_book_cover_for_book_id(self, book_id: str) -> None:
        """Upload cover and refresh book detail page."""
        bid = (book_id or "").strip()
        def _refresh():
            latest = self.data.get_book(bid) or {}
            if isinstance(latest, dict) and latest:
                self.show_book_detail(latest)
        self._prompt_and_upload_cover(bid, refresh_callback=_refresh)
    def _side_edit_book_details(self):
        """Enter in-place edit mode on the Book Info page (no popup)."""
        payload = getattr(self, "page_payload", {}) or {}
        book = payload.get("book") or getattr(self, "_current_book_detail", None) or {}
        if not isinstance(book, dict) or not book:
            messagebox.showinfo("Edit Book Details", "No book is currently open.")
            return

        self._current_book_detail = book
        self._book_edit_mode = True
        self._book_edit_vars = {}

        # Re-render the same Book Info page in edit mode
        # Suppress history - this is a mode change, not navigation
        self._nav_suppress_record = True
        self.show_book_detail(book)
    def _side_cancel_book_edit(self):
        """Cancel edit mode and return to normal Book Info view."""
        book = getattr(self, "_current_book_detail", None) or (getattr(self, "page_payload", {}) or {}).get("book")
        self._book_edit_mode = False
        self._book_edit_vars = {}
        if isinstance(book, dict) and book:
            # Suppress history - this is a mode change, not navigation
            self._nav_suppress_record = True
            self.show_book_detail(book)
    def _side_save_book_edit(self):
        """Save edits from in-place edit widgets into the catalog and persist immediately."""
        book = getattr(self, "_current_book_detail", None) or (getattr(self, "page_payload", {}) or {}).get("book")
        if not isinstance(book, dict) or not book:
            return

        bid = (book.get("book_id") or "").strip()
        if not bid:
            messagebox.showerror("Save Changes", "This book is missing a book_id.")
            return

        latest = self.data.get_book(bid) or {}
        if not isinstance(latest, dict):
            latest = dict(book)

        v = self._book_edit_vars or {}

        def _get_var(key: str, fallback: str = "") -> str:
            try:
                var = v.get(key)
                if var is None:
                    return fallback
                return (var.get() or "").strip()
            except Exception:
                return fallback

        updated = {}
        updated["title"] = _get_var("title", (latest.get("title") or "").strip())
        updated["author"] = _get_var("author", (latest.get("author") or "").strip())

        # ISBN shown on page
        updated["isbn"] = _get_var("isbn", (latest.get("isbn") or "").strip())

        # Genre dropdown (with Add new genre… option)
        genre_val = _get_var("genre", (latest.get("genre") or "").strip())
        if genre_val == "Add new genre…":
            new_g = simpledialog.askstring("Add Genre", "Enter new genre name:")
            if new_g:
                genre_val = new_g.strip().title()
                # Persist the new genre immediately so it appears everywhere (browse genres, edit dropdown, etc.)
                try:
                    self.data.add_user_genre(genre_val)
                except Exception:
                    pass
            else:
                genre_val = (latest.get("genre") or "").strip()
        updated["genre"] = genre_val

        # Tags - prefer backend data (tags editor modifies backend directly)
        # Only fall back to edit vars if backend has no tags
        try:
            backend_tags = self.data.get_tags(bid)
            if backend_tags:
                tags_list = backend_tags
            else:
                # Fallback to edit vars (comma-separated -> list)
                tags_raw = _get_var("tags", "")
                tags_list = [t.strip() for t in tags_raw.split(",") if t.strip()]
        except Exception:
            # Fallback to edit vars on any error
            tags_raw = _get_var("tags", "")
            tags_list = [t.strip() for t in tags_raw.split(",") if t.strip()]
        updated["tags"] = tags_list

        # Description Text widget (editable in place)
        desc_widget = v.get("description_widget")
        if desc_widget is not None:
            try:
                updated["description"] = desc_widget.get("1.0", "end").strip()
            except Exception:
                pass

        # Persist
        latest.update(updated)
        self.data.catalog[bid] = latest
        try:
            self.data.save()
        except Exception as e:
            messagebox.showerror("Save Changes", f"Could not save changes.\n\n{e}")
            return

        # Update last_updated timestamp in all collections containing this book
        # This enables "Last Updated" sort to work correctly
        try:
            for col in self._collections_all():
                col_book_ids = self._collection_book_ids(col)
                if bid in col_book_ids:
                    col_name = (col.get("name") or "").strip()
                    if col_name:
                        self.data.touch_collection_book(col_name, bid)
        except Exception:
            pass  # Don't fail the save if timestamp update fails

        self._book_edit_mode = False
        self._book_edit_vars = {}
        latest = self._ensure_book_origin(latest)
        self._current_book_detail = latest
        # Suppress history - this is returning from edit mode, not navigation
        self._nav_suppress_record = True
        self.show_book_detail(latest)
    def clear_active_widgets(self):
        for widget in self.active_widgets:
            try:
                widget.destroy()
            except tk.TclError:
                pass
        self.active_widgets.clear()
    def clear_page(self):
        self.close_side_menu()
        self._cancel_pending_page_jobs()
        self.clear_active_widgets()
        self.clear_canvas_text()
        for attr in ("_book_detail_genre", "_book_detail_tags"):
            info = getattr(self, attr, None)
            if info:
                try:
                    self.canvas.delete(info["item"])
                except Exception:
                    pass
                setattr(self, attr, None)


        self.placed_widgets.clear()
        self._active_scroll_canvas = None
    def _position_left_nav_stack(self):
        """Pin left-nav stack to bottom-left of the canvas, like the menu button."""
        btns = getattr(self, "_left_nav_buttons", None) or []
        if not btns:
            return

        layout = getattr(self, "_left_nav_layout", None) or {}
        left_pad = int(layout.get("left_pad", 35))
        bottom_pad = int(layout.get("bottom_pad", 35))
        btn_w = int(layout.get("btn_w", SHARED_NAV_BTN_WIDTH))
        btn_h = int(layout.get("btn_h", SHARED_NAV_BTN_HEIGHT))
        gap_y = int(layout.get("gap_y", SHARED_NAV_GAP_Y))

        self.canvas.update_idletasks()
        cw = max(self.canvas.winfo_width(), 1)
        ch = max(self.canvas.winfo_height(), 1)

        # bottom-left anchor point
        x = left_pad
        y = ch - bottom_pad

        # Place bottom->top
        for b in btns:
            try:
                if b.winfo_exists():
                    b.place(x=x, y=y, anchor="sw", width=btn_w, height=btn_h)
                    y -= (btn_h + gap_y)
            except Exception:
                pass

        self._raise_left_nav()
    def _raise_left_nav(self):
        """Ensure nav buttons appear above scroll containers and other widgets."""
        btns = getattr(self, "_left_nav_buttons", None) or []
        for b in btns:
            try:
                if b.winfo_exists():
                    b.lift()
            except Exception:
                pass
    def make_left_nav_stack(
            self,
            *,
            above: list[tuple[str, callable]] | None = None,
            home_text: str = "Home",
            home_cmd=None,
            show_home: bool = True,
            show_back: bool = False,
            back_text: str = "Back",
            back_command=None,
            extra_buttons: list[tuple[str, callable]] | None = None,
            # layout (now interpreted as margins/pixels relative to canvas)
            left_pad: int = 35,
            bottom_pad: int = 35,
            btn_w: int = SHARED_NAV_BTN_WIDTH,
            btn_h: int = SHARED_NAV_BTN_HEIGHT,
            gap_y: int = SHARED_NAV_GAP_Y,
            **_ignored,
    ) -> list[tk.Widget]:
        """
        Creates a vertical button stack and pins it to the bottom-left of the CANVAS.
        - Position is computed from current canvas size (fullscreen-safe).
        - Similar behavior to the menu button: recompute coords on resize.
        - Stores buttons so they can be repositioned later.
        """

        # --- resolve default commands ---
        if home_cmd is None:
            if hasattr(self, "go_home") and callable(getattr(self, "go_home")):
                home_cmd = self.go_home
            elif hasattr(self, "set_page") and callable(getattr(self, "set_page")):
                home_cmd = lambda: self.set_page("main_menu")
            else:
                home_cmd = lambda: None

        if back_command is None:
            if hasattr(self, "go_back") and callable(getattr(self, "go_back")):
                back_command = self.go_back
            else:
                back_command = lambda: None

        def _mk_btn(text: str, cmd):
            b = tk.Button(
                self.canvas,
                text=text,
                command=cmd,
                font=tkfont.Font(family=SHARED_FONT_CUSTOM, size=18),
                bg=SHARED_BUTTON1_BG_COLOR,
                fg=SHARED_BUTTON1_TEXT_COLOR,
                activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
                activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
                bd=SHARED_BUTTON_BORDER_WIDTH,
                relief="flat",
                cursor="hand2",
                highlightthickness=0,
            )
            self.active_widgets.append(b)
            return b

        # --- back button policy (same as your current logic) ---
        try:
            on_home = getattr(self, "current_page", "") in ("main", "home", "main_menu")
            depth = len(getattr(self, "_nav_history", []) or [])
            show_back = (not on_home) and depth >= 1
        except Exception:
            show_back = False

        # --- build stack bottom->top ---
        stack: list[tuple[str, callable]] = []
        if show_home:
            stack.append((home_text, home_cmd))
        if show_back:
            stack.append((back_text, back_command))

        extras: list[tuple[str, callable]] = []
        if above:
            extras.extend(above)
        if extra_buttons:
            extras.extend(extra_buttons)
        stack.extend(extras)

        # If we previously created nav buttons, destroy them (prevents duplicates)
        old = getattr(self, "_left_nav_buttons", None) or []
        for b in old:
            try:
                if b.winfo_exists():
                    b.destroy()
            except Exception:
                pass

        # Create buttons
        btns: list[tk.Widget] = []
        for text, cmd in stack:
            btns.append(_mk_btn(text, cmd))

        # Store layout info + refs for resize positioning
        self._left_nav_buttons = btns
        self._left_nav_layout = {
            "left_pad": int(left_pad),
            "bottom_pad": int(bottom_pad),
            "btn_w": int(btn_w),
            "btn_h": int(btn_h),
            "gap_y": int(gap_y),
        }

        # Initial position
        self._position_left_nav_stack()

        # Ensure it stays above scroll containers created later
        self.after_idle(self._raise_left_nav)

        return btns
    def make_home_button(self):
        return self.make_left_nav_stack(above=[], home_text="Home", home_cmd=self.go_home)
    def make_left_button(self, text: str, command, size: tuple[int, int], y: int):
        # keep signature for compatibility; ignore y to enforce global nav rule
        return self.make_left_nav_stack(above=[], home_text=text, home_cmd=command, btn_size=size)
    def make_button_box(self,text: str,command,design_pos: tuple[int, int],size: tuple[int, int] | None = None,font: tkfont.Font | None = None,colors: tuple[str, str, str, str] | None = None,border: int | None = None,):

        design_x, design_y = design_pos
        px_width, px_height = size if size else (SHARED_BUTTON_DEFAULT_WIDTH, SHARED_BUTTON_DEFAULT_HEIGHT)

        bg, fg, active_bg, active_fg = (
            colors if colors else
            (SHARED_SCROLL_BG_COLOR, SHARED_SEARCHBTN_BG_COLOR, FOCUS_PANEL_ACCENT_COLOR, SHARED_SEARCHBTN_BG_ONCLICK_COLOR)
        )
        border = border if border is not None else SHARED_BUTTON_BORDER_WIDTH

        frame = tk.Frame(
            self.canvas,
            width=px_width,
            height=px_height,
            bg=bg,
            highlightthickness=0,
            bd=0,
        )
        self.place_design(frame, design_x, design_y, anchor="center")
        frame.pack_propagate(False)

        btn = tk.Button(frame,
            text=text,
            command=lambda: self._safe_call(command),
            font=font or self.button_font,
            bg=bg, fg=fg,
            activebackground=active_bg, activeforeground=active_fg,
            bd=border, highlightthickness=0,
            relief="flat", takefocus=False)
        btn.pack(fill="both", expand=True)

        self.active_widgets.extend([frame, btn])
        return btn
    def make_button_box_right(self, text, command, design_pos, **kwargs):
        btn = self.make_button_box(text, command, design_pos, **kwargs)
        frame = btn.master

        # Remove the default placement
        self.placed_widgets.pop()

        self.place_design_right_bias(
            frame,
            design_pos[0],
            design_pos[1],
            anchor="center",
        )
        return btn
    def _render_genre_buttons(self,*,grid_frame,grid_canvas,genres: list[str],fs_like: bool,gap_x: int,gap_y: int,btn_min_w: int,btn_h: int,max_cols: int,):
        # clear old
        for child in grid_frame.winfo_children():
            child.destroy()

        if not genres:
            tk.Label(
                grid_frame,
                text="No genres found in this section yet.\nTry Sync Library to enrich genres.",
                bg=SHARED_EMPTYTABLE_BG_COLOR,
                fg=SHARED_EMPTYTABLE_TEXT_COLOR,
                font=(SHARED_FONT_CUSTOM, 26),
                justify="center",
                pady=40,
            ).pack(fill="both", expand=True)
            return

        avail_w = max(grid_canvas.winfo_width(), 1)

        cols_by_width = max(1, (avail_w + gap_x) // (btn_min_w + gap_x))
        cols = max(1, min(int(cols_by_width), max_cols))

        total_gap = gap_x * (cols - 1)
        btn_w = max(btn_min_w, (avail_w - total_gap) // cols)

        for c in range(cols):
            grid_frame.grid_columnconfigure(c, weight=1, uniform="genrecols")

        for i, genre in enumerate(genres):
            r = i // cols
            c = i % cols
            row_bg = SHARED_TABLE_BG_COLOR if r % 2 == 0 else SHARED_TABLE_ALTROW_BG_COLOR

            frame = tk.Frame(grid_frame, width=btn_w, height=btn_h, bg=row_bg, highlightthickness=0, bd=0)
            frame.grid(
                row=r, column=c,
                padx=(0 if c == 0 else gap_x, 0),
                pady=(0 if r == 0 else gap_y, 0),
                sticky="nsew",
            )
            frame.grid_propagate(False)

            btn = tk.Button(
                frame,
                text=genre,
                command=lambda g=genre: self.show_genre_page(g),
                font=self.genre_font,
                bg=BROWSEGENRES_TILE_BG_COLOR,
                fg=BROWSEGENRES_TILE_TEXT_COLOR,
                activebackground=BROWSEGENRES_TILE_BG_ONCLICK_COLOR,
                activeforeground=BROWSEGENRES_TILE_TEXT_ONCLICK_COLOR,
                bd=SHARED_BUTTON_BORDER_WIDTH,
                highlightthickness=0,
                relief="flat",
                takefocus=False,
                wraplength=btn_w - 20,
            )
            btn.pack(fill="both", expand=True)
            self.active_widgets.extend([frame, btn])
    def _make_scroll_container(self, *, relx=0.5, rely=0.5, relwidth=0.88, relheight=0.68, bg=THEME_COLOR8, top_inset: int = 0, sb_width: int = 14, content_pad_x: int = 0, content_pad_y: int = 0):
        """
        Creates a card container with a scrollable canvas inside.
        - top_inset reserves space at the top for a pinned header strip.
        Returns: (container, canvas, scroll_frame)
        """
        container = tk.Frame(self.canvas, bg=bg, bd=0, highlightthickness=0)
        container.place(relx=relx, rely=rely, anchor="center", relwidth=relwidth, relheight=relheight)

        canvas = tk.Canvas(container, highlightthickness=0, bd=0, bg=bg)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview, width=sb_width)

        scroll_frame = tk.Frame(canvas, bg=bg)
        scroll_frame.grid_columnconfigure(0, weight=1)

        window_id = canvas.create_window(
            (content_pad_x, content_pad_y),
            window=scroll_frame,
            anchor="nw",
        )

        # ✅ store ids so renderers can force-width sync anytime
        canvas._inner_window_id = window_id
        canvas._inner_frame = scroll_frame

        def _sync_scrollregion(_evt=None):
            try:
                canvas.configure(scrollregion=canvas.bbox("all"))
            except Exception:
                pass

        scroll_frame.bind("<Configure>", _sync_scrollregion)

        def _force_inner_width(width_px: int):
            inner_w = max(width_px - (2 * content_pad_x), 1)
            try:
                canvas.itemconfig(window_id, width=inner_w)
            except Exception:
                pass
            try:
                scroll_frame.configure(width=inner_w)
            except Exception:
                pass

        def _on_canvas_configure(event):
            _force_inner_width(event.width)

        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        self._register_scroll_canvas(canvas)

        canvas.place(x=0, y=top_inset, relwidth=1.0, relheight=1.0, height=-top_inset)
        scrollbar.place(relx=1.0, x=0, y=top_inset, relheight=1.0, height=-top_inset, anchor="ne")

        # ✅ IMPORTANT: after layout settles, force sync once
        def _late_sync():
            if canvas.winfo_exists():
                _force_inner_width(canvas.winfo_width())
                _sync_scrollregion()

        canvas.after_idle(_late_sync)

        self.active_widgets.extend([container, canvas, scrollbar, scroll_frame])
        return container, canvas, scroll_frame

    ## Side Menu
    # --- Side Menu core ---
    MENU_BTN_H_PX = 60
    MENU_BTN_MAX_PX = 60
    MENU_BTN_X_DESIGN = 1140
    MENU_BTN_Y_DESIGN = 820

    def _init_side_menu_assets(self):
        """Load PIL assets + mount the always-available menu button."""
        if not MENU_BTN_IMG.exists():
            raise FileNotFoundError(f"Menu button image not found: {MENU_BTN_IMG}")
        if not SIDE_MENU_BG_IMG.exists():
            raise FileNotFoundError(f"Side menu bg image not found: {SIDE_MENU_BG_IMG}")

        # Load PIL once
        self._menu_btn_pil = Image.open(MENU_BTN_IMG).convert("RGBA")
        self._side_menu_bg_pil = Image.open(SIDE_MENU_BG_IMG).convert("RGBA")

        # Create canvas image item ONCE
        if self._menu_btn_item is None:
            self._menu_btn_item = self.canvas.create_image(
                0, 0,
                anchor="se",
                tags=("menu_btn",)
            )
            self.canvas.tag_bind(
                self._menu_btn_item,
                "<Button-1>",
                lambda e: self.toggle_side_menu()
            )

        # Render image into the existing item
        self._refresh_menu_button_image()

        # Position it
        self._position_menu_button()
    def _refresh_menu_button_image(self):
        """Scale menu button to a fixed pixel height (easy to control)."""
        if self._menu_btn_pil is None:
            return

        target_h = int(getattr(self, "MENU_BTN_H_PX", 110))
        max_h = int(getattr(self, "MENU_BTN_MAX_PX", 160))
        target_h = max(24, min(max_h, target_h))

        pil = self._menu_btn_pil
        w0, h0 = pil.size
        if h0 <= 0:
            return

        scale = target_h / h0
        target_w = max(1, int(w0 * scale))

        resized = pil.resize((target_w, target_h), Image.LANCZOS)
        self._menu_btn_tk = ImageTk.PhotoImage(resized)

        try:
            self.canvas.itemconfigure(self._menu_btn_item, image=self._menu_btn_tk)
        except Exception:
            pass
    def _position_menu_button(self, *, margin_x: int = 24, margin_y: int = 24):
        if getattr(self, "_menu_btn_item", None) is None:
            return

        self.canvas.update_idletasks()
        cw = max(self.canvas.winfo_width(), 1)
        ch = max(self.canvas.winfo_height(), 1)

        x = cw - margin_x
        y = ch - margin_y

        try:
            self.canvas.coords(self._menu_btn_item, x, y)
        except Exception:
            pass
    def toggle_side_menu(self):
        if getattr(self, "_side_menu_open", False):
            self.close_side_menu()
        else:
            self.open_side_menu()
    def open_side_menu(self):
        if getattr(self, "_side_menu_open", False):
            return
        self._side_menu_open = True

        self.update_idletasks()

        x = self.winfo_rootx()
        y = self.winfo_rooty()
        w = max(self.winfo_width(), 1)
        h = max(self.winfo_height(), 1)

        # ---- 1) dim overlay (transparent) ----
        dim = tk.Toplevel(self)
        dim.overrideredirect(True)
        dim.geometry(f"{w}x{h}+{x}+{y}")
        dim.configure(bg="black")
        try:
            dim.attributes("-alpha", 0.35)
        except Exception:
            pass

        # IMPORTANT: do NOT make the dimmer topmost
        try:
            dim.attributes("-topmost", False)
        except Exception:
            pass

        dim.bind("<Button-1>", lambda e: self.close_side_menu())
        self._side_menu_dim = dim

        # ---- 2) panel window (NOT transparent) ----
        panel_w = max(240, int(w * 0.33))
        panel = tk.Toplevel(self)
        panel.overrideredirect(True)
        panel.geometry(f"{panel_w}x{h}+{x + w - panel_w}+{y}")

        # panel SHOULD be above everything
        try:
            panel.attributes("-topmost", True)
        except Exception:
            pass

        panel.bind("<Button-1>", lambda e: "break")
        self._side_menu_panel_win = panel

        self._side_menu_bg_lbl = tk.Label(panel, bd=0, highlightthickness=0)
        self._side_menu_bg_lbl.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        self._side_menu_bg_lbl.bind("<Button-1>", lambda e: "break")

        self._refresh_side_menu_bg_image()
        self._build_side_menu_buttons()

        # ✅ FORCE correct stacking: dim behind, panel in front
        try:
            dim.lift(self)  # lift dim above root
            panel.lift(dim)  # lift panel above dim
        except Exception:
            pass

        # sometimes macOS needs a second nudge
        self.after_idle(lambda: (panel.lift(), None))

    def _refresh_side_menu_bg_image(self):
        """Resize side_menu.png to the PANEL size (1/3 window)."""
        if self._side_menu_bg_pil is None:
            return
        if not (self._side_menu_panel_win and self._side_menu_panel_win.winfo_exists()):
            return
        if not (self._side_menu_bg_lbl and self._side_menu_bg_lbl.winfo_exists()):
            return

        self._side_menu_panel_win.update_idletasks()
        w = max(self._side_menu_panel_win.winfo_width(), 1)
        h = max(self._side_menu_panel_win.winfo_height(), 1)
        size = (w, h)

        if self._side_menu_bg_last_size == size and self._side_menu_bg_tk is not None:
            return

        pil = ImageOps.fit(
            self._side_menu_bg_pil,
            size,
            method=Image.LANCZOS,
            centering=(0, 0.5),
        )
        self._side_menu_bg_tk = ImageTk.PhotoImage(pil)
        self._side_menu_bg_last_size = size
        try:
            self._side_menu_bg_lbl.config(image=self._side_menu_bg_tk)
        except Exception:
            pass
    def close_side_menu(self):
        self._side_menu_open = False

        # destroy panel first (so it doesn't linger above dim)
        if self._side_menu_panel_win and self._side_menu_panel_win.winfo_exists():
            try:
                self._side_menu_panel_win.destroy()
            except Exception:
                pass

        if self._side_menu_dim and self._side_menu_dim.winfo_exists():
            try:
                self._side_menu_dim.destroy()
            except Exception:
                pass

        self._side_menu_dim = None
        self._side_menu_panel_win = None
        self._side_menu_bg_lbl = None
        self._side_menu_bg_last_size = None
    def _side_menu_actions_for_page(self) -> list[tuple[str, Callable[[], Any]]]:
        page = getattr(self, "current_page", "") or ""
        specs = self.side_menu_map.get(page, [])

        # Dynamic Book Info menu: show Save/Cancel while editing
        if page == "book_detail" and getattr(self, "_book_edit_mode", False):
            specs = [
                ("Save Changes", self._side_save_book_edit),
                ("Cancel", self._side_cancel_book_edit),
                ("Back", self.go_back),
                ("Home", self.go_home),
            ]

        # If empty -> show ONLY the background (no buttons)
        if not specs:
            return []

        actions: list[tuple[str, Callable[[], Any]]] = []

        for label, fn in specs:
            def _wrapped(f=fn):
                self.close_side_menu()
                return self._safe_call(f)

            actions.append((label, _wrapped))

        return actions
    def _build_side_menu_buttons(self):
        """Builds the vertical options stack on top of side_menu.png."""
        if not (self._side_menu_bg_lbl and self._side_menu_bg_lbl.winfo_exists()):
            return

        # clear previous button widgets (if rebuilt)
        for child in list(self._side_menu_bg_lbl.winfo_children()):
            try:
                child.destroy()
            except Exception:
                pass

        actions = self._side_menu_actions_for_page()
        if not actions:
            return


        # layout
        top_pad = 120
        x_pad = 26
        btn_h = 52
        gap = 14

        # Button style (ties to your theme)
        btn_font = (SHARED_FONT_BUTTON, 20)

        for i, (label, cmd) in enumerate(actions):
            y = top_pad + i * (btn_h + gap)

            b = tk.Button(
                self._side_menu_bg_lbl,
                text=label,
                command=cmd,
                bg=SHARED_SIDEMENU_BTN_BG_COLOR,
                fg=SHARED_SIDEMENU_BTN_TEXT_COLOR,
                activebackground=SHARED_SIDEMENU_BTN_BG_ONCLICK_COLOR,
                activeforeground=SHARED_SIDEMENU_BTN_TEXT_ONCLICK_COLOR,
                bd=0,
                highlightthickness=0,
                relief="flat",
                takefocus=False,
                font=btn_font,
            )
            b.place(x=x_pad, y=y, relwidth=1.0, width=-(2 * x_pad), height=btn_h)

            self.active_widgets.append(b)
    def _position_side_menu_windows(self):
        """Keep dim overlay + panel aligned to the root window."""
        if not getattr(self, "_side_menu_open", False):
            return

        self.update_idletasks()

        x = self.winfo_rootx()
        y = self.winfo_rooty()
        w = max(self.winfo_width(), 1)
        h = max(self.winfo_height(), 1)

        # dim overlay covers entire app window
        if self._side_menu_dim and self._side_menu_dim.winfo_exists():
            self._side_menu_dim.geometry(f"{w}x{h}+{x}+{y}")

        # panel is 1/3 width, docked right
        if self._side_menu_panel_win and self._side_menu_panel_win.winfo_exists():
            panel_w = max(240, int(w * 0.33))
            panel_x = x + w - panel_w
            self._side_menu_panel_win.geometry(f"{panel_w}x{h}+{panel_x}+{y}")

    # ---------- SHARED BOOK SORTING AND VIEWING HELPERS ----------
    def _populate_book_table(self,scroll_frame: tk.Frame,rows: list[dict],
            col_order: tuple[str, str, str],header_labels: tuple[str, str, str],*,query_label: str = "",):
        # Clear any existing contents
        for child in scroll_frame.winfo_children():
            child.destroy()

        header_font = SHARED_TABLE_HEADER_FONT
        row_font = SHARED_TABLE_ROW_FONT

        # Column stretch
        scroll_frame.grid_columnconfigure(0, weight=3, minsize=150)
        scroll_frame.grid_columnconfigure(1, weight=3, minsize=280)
        scroll_frame.grid_columnconfigure(2, weight=1, minsize=80)

        # Headers
        for col, label in enumerate(header_labels):
            tk.Label(
                scroll_frame,
                text=label,
                font=header_font,
                anchor="w",
                bg=SHARED_TABLE_BG_COLOR,
                fg=FOCUS_PANEL_TEXT_COLOR,
                padx=10,
                pady=5,
            ).grid(row=0, column=col, sticky="we")

        if not rows:
            tk.Label(
                scroll_frame,
                text="No books found.",
                font=(SHARED_FONT_CUSTOM, 18),
                anchor="center",
                bg=SHARED_TABLE_BG_COLOR,
                fg=FOCUS_PANEL_TEXT_COLOR,
                padx=10,
                pady=20,
            ).grid(row=1, column=0, columnspan=3, sticky="we")
            return

        # capture once so clicks always return to the same list
        rows_for_back = list(rows)

        for idx, row in enumerate(rows_for_back, start=1):
            author, title, year = self._get_display_fields(row)
            field_map = {"title": title, "author": author, "year": year}
            bg_color = SHARED_TABLE_ALTROW_BG_COLOR if idx % 2 == 0 else SHARED_TABLE_BG_COLOR

            # (Optional) full-row frame makes the whole stripe feel clickable
            row_frame = tk.Frame(scroll_frame, bg=bg_color, highlightthickness=0, bd=0)
            row_frame.grid(row=idx, column=0, columnspan=3, sticky="we")
            row_frame.grid_columnconfigure(0, weight=3, minsize=150)
            row_frame.grid_columnconfigure(1, weight=3, minsize=280)
            row_frame.grid_columnconfigure(2, weight=1, minsize=80)

            labels: list[tk.Label] = []
            for col, field_key in enumerate(col_order):
                lbl = tk.Label(
                    row_frame,
                    text=field_map[field_key],
                    font=row_font,
                    anchor="w",
                    bg=SHARED_TABLE_BG_COLOR,
                    fg=FOCUS_PANEL_TEXT_COLOR,
                    padx=15,
                    pady=8,
                    cursor="hand2",
                )
                lbl.grid(row=0, column=col, sticky="we")
                labels.append(lbl)

            # Click opens via helper (preserves “back to results”)
            def _open(_e, b=row, rows=rows_for_back, q=query_label):
                self._open_book_from_list(b, rows, q)

            # bind row + cells so clicking anywhere works
            row_frame.bind("<Button-1>", _open)
            for lbl in labels:
                lbl.bind("<Button-1>", _open)
    def _year_key_from_row(self, r: dict) -> int:
        publish_date = (r.get("publish_date") or r.get("date_published") or "").strip()
        if publish_date:
            y_str = publish_date.split("-")[0]
            try:
                return int(y_str)
            except ValueError:
                return 0
        return 0
    def _get_sort_key_func(self, field: str, reverse: bool = False):
        """
        Returns a sort key function for any field name.
        This allows adding new fields without updating the sort logic.
        If reverse is True, returns a key that sorts in reverse order.
        """
        field = (field or "").strip().lower()

        if field == "author":
            base_func = lambda r: self._author_display_and_sort_key(r)[1]
        elif field == "year":
            # Year sorts by numeric value
            base_func = lambda r: self._year_key_from_row(r) if self._year_key_from_row(r) else 0
        elif field == "genre":
            base_func = lambda r: (r.get("genre") or "").strip().lower()
        elif field == "updated" or field == "last updated":
            # For collections
            base_func = lambda r: (r.get("_collection_updated_ts") or r.get("updated_at") or 0)
        elif field == "read":
            base_func = lambda r: 0 if r.get("read") else 1  # Read items first
        else:
            # Default to title
            base_func = lambda r: (r.get("title") or "").strip().lower()

        return base_func
    def _get_filter_first_char(self, book: dict, field: str) -> str:
        """Get the first character category for filtering based on a field."""
        field = (field or "").strip().lower()

        if field == "author" or field == "author (last name)":
            # Get author last name
            last = (book.get("last_name") or "").strip()
            if not last:
                creators = (book.get("creators") or "").strip()
                if creators:
                    parts = creators.split()
                    last = parts[-1] if parts else ""
            text = last
        elif field == "year":
            # Get year - use first digit
            year = (book.get("_year") or "").strip()
            if not year:
                publish_date = (book.get("publish_date") or book.get("date_published") or "").strip()
                if publish_date:
                    year = publish_date.split("-")[0]
            text = year
        else:
            # Default to title
            text = (book.get("title") or "").strip()

        if not text:
            return "~"
        first = text[0].upper()
        if first.isalpha():
            return first
        elif first.isdigit():
            return "#"
        else:
            return "~"
    def _sort_books_multi(self, rows: list[dict], primary: str, secondary: str | None = None, reverse: bool = False) -> list[dict]:
        """
        Sort books by primary field, then by secondary field.
        Both fields can be any column name (Title, Author, Year, Genre, etc.)
        If reverse is True, reverses the entire sort order.
        Numbers/symbols go at the end for A-Z, at the beginning for Z-A.
        """
        if not rows:
            return rows

        primary = (primary or "Title").strip()
        secondary = (secondary or "").strip()

        # Build composite key function
        primary_key = self._get_sort_key_func(primary)

        if secondary and secondary.lower() != primary.lower():
            secondary_key = self._get_sort_key_func(secondary)
            sorted_rows = sorted(rows, key=lambda r: (primary_key(r), secondary_key(r)))
        else:
            sorted_rows = sorted(rows, key=primary_key)

        if reverse:
            sorted_rows = list(reversed(sorted_rows))

        return sorted_rows
    def _sort_books(self, rows: list[dict], mode: str) -> list[dict]:
        """Legacy single-sort function for backward compatibility."""
        return self._sort_books_multi(rows, mode, "Title")
    def _make_sort_and_view_controls(self, parent: tk.Widget, *, bg: str = SORT_VIEW_BG, pad_x: int | None = None, pad_y: int | None = None, x_pad: int | None = None, y_pad: int | None = None,
                                     default_view: str = "grid", default_sort: str = "Title", sort_values: tuple[str, ...] = ("Title", "Author", "Year")):
        """
        Pinned header controls:
        - LEFT: View: [Grid] [List]
        - RIGHT: Sort by: [Title/Author/Year]

        Accepts either pad_x/pad_y OR x_pad/y_pad (backward compatible).
        Returns: (sort_var, view_var, view_btns, secondary_sort_var, secondary_sort_reverse_var)

        secondary_sort_var: Set by clicking column headers in list view.
        secondary_sort_reverse_var: Boolean - True if reverse sort (Z-A), False if A-Z.
        """
        if pad_x is None:
            pad_x = 18 if x_pad is None else x_pad
        if pad_y is None:
            pad_y = 10 if y_pad is None else y_pad

        sort_var = tk.StringVar(value=default_sort)
        view_var = tk.StringVar(value=default_view)
        secondary_sort_var = tk.StringVar(value="")  # Empty means no secondary sort
        secondary_sort_reverse_var = tk.BooleanVar(value=False)  # False = A-Z, True = Z-A

        # ✅ bar fills the whole header area (no outer padx/pady here)
        bar = tk.Frame(parent, bg=bg, highlightthickness=0, bd=0)
        bar.pack(fill="both", expand=True)
        self.active_widgets.append(bar)

        # ✅ padding applies to the content only (like your desired screenshot)
        inner = tk.Frame(bar, bg=bg, highlightthickness=0, bd=0)
        inner.pack(fill="both", expand=True, padx=pad_x, pady=pad_y)
        self.active_widgets.append(inner)

        left = tk.Frame(inner, bg=bg, highlightthickness=0, bd=0)
        right = tk.Frame(inner, bg=bg, highlightthickness=0, bd=0)
        left.pack(side="left", anchor="w")
        right.pack(side="right", anchor="e")
        self.active_widgets.extend([left, right])

        lbl_font = (SHARED_FONT_TABLE, 18)
        ui_font = (SHARED_FONT_TABLE, 16)

        # LEFT: View controls
        tk.Label(left, text="View:", bg=SHARED_MAINHEADER_BG_COLOR, fg=SHARED_MAINHEADER_SUBTEXT_COLOR, font=lbl_font).pack(side="left", padx=(0, 12))
        view_btns = tk.Frame(left, bg=SHARED_MAINHEADER_BG_COLOR, highlightthickness=0, bd=0)
        view_btns.pack(side="left")
        self.active_widgets.append(view_btns)

        # RIGHT: Sort controls
        tk.Label(right, text="Sort by:", bg=SHARED_MAINHEADER_BG_COLOR, fg=SHARED_MAINHEADER_SUBTEXT_COLOR, font=lbl_font).pack(side="left", padx=(0, 12))

        sort_combo = ttk.Combobox(
            right,
            textvariable=sort_var,
            values=sort_values,
            state="readonly",
            width=12,
            font=ui_font,
            style="Theme.TCombobox",
        )
        sort_combo.pack(side="left")
        self.active_widgets.append(sort_combo)

        # Reset secondary sort when primary sort changes
        def _on_primary_sort_change(*_):
            secondary_sort_var.set("")
            secondary_sort_reverse_var.set(False)
        sort_var.trace_add("write", _on_primary_sort_change)

        return sort_var, view_var, view_btns, secondary_sort_var, secondary_sort_reverse_var
    def _make_bubble_radio(self, parent, *, text, variable, value, command, bg=SHARED_RADIO_BG_COLOR):
        rb = tk.Radiobutton(
            parent,
            text=text,
            variable=variable,
            value=value,
            indicatoron=False,
            font=(SHARED_FONT_TABLE, 16),
            bg=bg,
            fg=SHARED_RADIO_TEXT_COLOR,
            selectcolor=SHARED_MAINHEADER_BG_COLOR,
            activebackground=bg,
            activeforeground=SHARED_ALPHA_MUTED_TEXT_COLOR,
            bd=1,
            relief="solid",
            padx=10,
            pady=4,
            command=command,
            highlightthickness=0,
        )
        rb.pack(side="left", padx=6)
        return rb
    def _make_alphabet_filter_bar(self,*,books: list[dict],filter_field: str = "Title",letter_filter: str | None = None,
        on_filter_change: Callable[[str | None, str], None],show_filter_dropdown: bool = True,rely: float = 0.2,) -> tk.Frame:
        """
        Create an alphabet filter bar that can be reused across pages.
        
        Args:
            books: List of books to count letters from
            filter_field: Current filter field ("Title", "Author (Last Name)", "Year")
            letter_filter: Currently selected letter filter (None for all)
            on_filter_change: Callback(letter_filter, filter_field) when filter changes
            show_filter_dropdown: Whether to show the "Filter by:" dropdown
            rely: Relative Y position for the TOP of the bar
            
        Returns:
            The alphabet bar frame widget
        """
        # Count books per letter category based on selected filter field
        letter_counts: dict[str, int] = {}
        for book in books:
            cat = self._get_filter_first_char(book, filter_field)
            letter_counts[cat] = letter_counts.get(cat, 0) + 1

        # Build the alphabet bar - use anchor="n" so rely is the TOP edge
        alphabet_bar = tk.Frame(self.canvas, bg=ALPHABAR_BORDER_COLOR, highlightthickness=0, bd=0)
        alphabet_bar.place(relx=0.5, rely=rely, anchor="n", relwidth=0.88, height=36)
        self.active_widgets.append(alphabet_bar)

        # Inner frame for centering content
        inner = tk.Frame(alphabet_bar, bg=SHARED_ALPHABAR_BG_COLOR, highlightthickness=0, bd=0)
        inner.pack(expand=True, fill="x", padx=10)
        self.active_widgets.append(inner)

        btn_font = (SHARED_FONT_TABLE, 12)

        # Filter dropdown on the left (optional)
        if show_filter_dropdown:
            filter_var = tk.StringVar(value=filter_field)
            filter_label = tk.Label(
                inner,
                text="Filter by:",
                font=(SHARED_FONT_TABLE, 11),
                bg=SHARED_ALPHABAR_BG_COLOR,
                fg=SHARED_ALPHA_CLICKABLE_TEXT_COLOR,
                padx=4,
                pady=4,
            )
            filter_label.pack(side="left", padx=(0, 5))
            self.active_widgets.append(filter_label)

            filter_combo = ttk.Combobox(
                inner,
                textvariable=filter_var,
                values=("Title", "Author (Last Name)", "Year"),
                state="readonly",
                width=16,
                font=(SHARED_FONT_TABLE, 10),
            )
            filter_combo.pack(side="left", padx=(0, 15))
            self.active_widgets.append(filter_combo)

            def _on_filter_field_change(event=None):
                new_field = filter_var.get()
                # Reset letter filter when changing field
                on_filter_change(None, new_field)

            filter_combo.bind("<<ComboboxSelected>>", _on_filter_field_change)

        # All the possible categories in order
        categories = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["#", "~"]

        for cat in categories:
            has_books = cat in letter_counts and letter_counts[cat] > 0
            is_selected = (letter_filter == cat)

            if has_books:
                # Clickable button
                if is_selected:
                    # Selected state - highlighted
                    btn = tk.Label(
                        inner,
                        text=cat,
                        font=btn_font,
                        bg=SHARED_ALPHA_SELECTED_BG_COLOR,
                        fg=SHARED_ALPHA_SELECTED_TEXT_COLOR,
                        padx=6,
                        pady=4,
                        cursor="hand2",
                    )
                else:
                    # Normal clickable state
                    btn = tk.Label(
                        inner,
                        text=cat,
                        font=btn_font,
                        bg=SHARED_ALPHA_CLICKABLE_BG_COLOR,
                        fg=SHARED_ALPHA_CLICKABLE_TEXT_COLOR,
                        padx=6,
                        pady=4,
                        cursor="hand2",
                    )

                def _on_click(e=None, c=cat, ff=filter_field):
                    if letter_filter == c:
                        # Clicking same letter clears filter
                        on_filter_change(None, ff)
                    else:
                        on_filter_change(c, ff)

                btn.bind("<Button-1>", _on_click)

                # Hover effect for non-selected buttons
                if not is_selected:
                    def _on_enter(e, lbl=btn):
                        lbl.configure(bg=SHARED_ALPHA_HOVER_BG_COLOR, fg=SHARED_ALPHA_HOVER_TEXT_COLOR)
                    def _on_leave(e, lbl=btn):
                        lbl.configure(bg=SHARED_ALPHA_CLICKABLE_BG_COLOR, fg=SHARED_ALPHA_CLICKABLE_TEXT_COLOR)
                    btn.bind("<Enter>", _on_enter)
                    btn.bind("<Leave>", _on_leave)
            else:
                # Disabled/empty state - grayed out
                btn = tk.Label(
                    inner,
                    text=cat,
                    font=btn_font,
                    bg=SHARED_ALPHA_MUTED_BG_COLOR,
                    fg=SHARED_ALPHA_MUTED_TEXT_COLOR,
                    padx=6,
                    pady=4,
                )

            btn.pack(side="left", padx=1)
            self.active_widgets.append(btn)

        return alphabet_bar
    def _render_books_grid_or_list(self,*,canvas: tk.Canvas,scroll_frame: tk.Frame,books: list[dict],
        sort_var: tk.StringVar,view_var: tk.StringVar,view_btns: tk.Widget,context_label: str,panel_bg: str, row_text_fg: str = GENREPAGE_ROW_FG_COLOR,
        cols: int = 5,is_collection: bool = False,collection_name: str | None = None,secondary_sort_var: tk.StringVar | None = None,
        secondary_sort_reverse_var: tk.BooleanVar | None = None,):
        """
        One shared renderer used by Genre / View All / Search Results.
        - Sort: Primary from dropdown + Secondary from clicking column headers
        - View: grid/list (grid shows covers)
        - Click: opens book detail and preserves back list + label
        - Clickable headers toggle A-Z / Z-A sort
        """

        # Create a dummy secondary_sort_var if not provided (backward compat)
        if secondary_sort_var is None:
            secondary_sort_var = tk.StringVar(value="")
        if secondary_sort_reverse_var is None:
            secondary_sort_reverse_var = tk.BooleanVar(value=False)

        def _add_book_tile(holder: tk.Frame, book: dict, row_bg: str, rows_for_back: list[dict]):
            cell = tk.Frame(holder, bg=row_bg, highlightthickness=0, bd=0, cursor="hand2")
            # caller grids this cell

            title = self._unescape_entities(book.get("title") or "Untitled").strip()
            book_id = str((book.get("book_id") or book.get("id") or "")).strip()
            cover_path = self.data.get_cover_path(book_id) if book_id else None

            def _open(_e=None, b=book, rows=rows_for_back):
                self._open_book_from_list(b, rows, context_label)

            if cover_path and hasattr(cover_path, "exists") and cover_path.exists():
                pil = Image.open(cover_path).convert("RGB")
                pil.thumbnail((cover_w, cover_h), Image.LANCZOS)
                photo = ImageTk.PhotoImage(pil)
                self._page_img_refs.append(photo)

                cover_lbl = tk.Label(cell, image=photo, bg=row_bg, bd=0, highlightthickness=0, cursor="hand2")
                cover_lbl.pack()
                cover_lbl.bind("<Button-1>", _open)
            else:
                ph = tk.Canvas(cell, width=cover_w, height=cover_h, bg=SHARED_BLANKCOVER_BG_COLOR,
                               highlightthickness=0, cursor="hand2")
                ph.create_text(
                    cover_w // 2, cover_h // 2,
                    text="No Cover",
                    fill=SHARED_BLANKCOVER_TEXT_COLOR,
                    font=(SHARED_FONT_CUSTOM, 16),
                )
                ph.pack()
                ph.bind("<Button-1>", _open)

            title_lbl = tk.Label(
                cell,
                text=title,
                bg=row_bg,
                fg=SHARED_SCROLLROW_TEXT_COLOR,
                font=(SHARED_FONT_TABLE, 16),
                wraplength=title_wrap,
                justify="center",
                cursor="hand2",
            )
            self._book_detail_title_lbl = title_lbl

            title_lbl.pack(pady=(8, 0))
            title_lbl.bind("<Button-1>", _open)
            cell.bind("<Button-1>", _open)

            return cell
        def _norm_genre(g: str) -> str:
            g = (g or "").strip()
            return g if g else "Unknown"
        def _collection_updated_ts(book: dict) -> float:
            if not (is_collection and collection_name):
                return 0.0
            bid = str((book.get("book_id") or book.get("id") or "")).strip()
            if not bid:
                return 0.0
            try:
                return float(self.data.get_collection_last_updated(collection_name, bid) or 0.0)
            except Exception:
                return 0.0
        def _sorted_rows(mode: str, secondary: str = "", reverse: bool = False) -> list[dict]:
            """Sort books by primary mode, then by secondary field if set.
            If reverse is True, reverses the sort order (Z-A instead of A-Z).
            """
            mode = (mode or "").strip()
            secondary = (secondary or "").strip()

            # Special handling for collection-specific sorts
            if is_collection and mode == "Genre":
                base_sorted = sorted(books,
                              key=lambda b: (_norm_genre(b.get("genre")).lower(), (b.get("title") or "").lower()))
                if secondary and secondary.lower() != "genre":
                    # Apply secondary sort within each genre group
                    sec_key = self._get_sort_key_func(secondary)
                    result = sorted(base_sorted, key=lambda b: (_norm_genre(b.get("genre")).lower(), sec_key(b)))
                else:
                    result = base_sorted
                return list(reversed(result)) if reverse else result
            if is_collection and mode == "Last Updated":
                base_sorted = sorted(books, key=lambda b: (_collection_updated_ts(b), (b.get("title") or "").lower()),
                              reverse=True)
                return list(reversed(base_sorted)) if reverse else base_sorted

            # Use multi-level sort for standard modes
            return self._sort_books_multi(books, mode, secondary if secondary else "Title", reverse=reverse)

        # --- layout constants (same feel as your genre page) ---
        cover_w, cover_h = 130, 190
        pad_x, pad_y = 24, 0
        title_wrap = cover_w + 40

        def _force_canvas_window_width():
            wid = getattr(canvas, "_inner_window_id", None)
            if wid is None:
                return
            try:
                canvas.itemconfig(wid, width=max(canvas.winfo_width(), 1))
            except Exception:
                pass
            try:
                scroll_frame.configure(width=max(canvas.winfo_width(), 1))
            except Exception:
                pass
        def clear_scroll_contents():
            for child in scroll_frame.winfo_children():
                child.destroy()
        def render_grid_view(mode: str):
            _force_canvas_window_width()
            clear_scroll_contents()

            rows_sorted = _sorted_rows(mode)

            try:
                scroll_frame.grid_columnconfigure(0, weight=1)
            except Exception:
                pass

            # --- GROUPED GRID (collection-only, sort=Genre) ---
            if is_collection and mode == "Genre":
                # group in order
                groups: list[tuple[str, list[dict]]] = []
                current_g = None
                bucket: list[dict] = []

                for b in rows_sorted:
                    g = _norm_genre(b.get("genre"))
                    if current_g is None:
                        current_g = g
                    if g != current_g:
                        groups.append((current_g, bucket))
                        current_g = g
                        bucket = []
                    bucket.append(b)
                if current_g is not None:
                    groups.append((current_g, bucket))

                r = 0
                stripe_i = 0

                for genre, g_books in groups:
                    # short header row
                    hdr = tk.Frame(scroll_frame, bg=BROWSEGENRES_PANEL_BG_COLOR, highlightthickness=0, bd=0)
                    hdr.grid(row=r, column=0, sticky="we", padx=0, pady=(0, 0))

                    hdr.grid_columnconfigure(0, weight=1)

                    tk.Label(
                        hdr,
                        text=genre.upper(),
                        bg=OPENCOLL_HEADER_BG_COLOR,
                        fg=OPENCOLL_HEADER_FG_COLOR,
                        font=(SHARED_FONT_TABLE, 16, "bold"),
                        anchor="w",
                        padx=18,
                        pady=6,  # ✅ shorter than book rows
                    ).grid(row=0, column=0, sticky="we")

                    r += 1

                    # render this genre's books in rows of `cols`
                    chunks = [g_books[i:i + cols] for i in range(0, len(g_books), cols)]
                    for row_books in chunks:
                        row_bg = SHARED_TABLE_ALTROW_BG_COLOR if (stripe_i % 2 == 0) else panel_bg
                        stripe_i += 1

                        stripe = tk.Frame(scroll_frame, bg=row_bg, highlightthickness=0, bd=0)
                        stripe.grid(row=r, column=0, sticky="nsew", padx=0, pady=(0, 0))
                        stripe.grid_columnconfigure(0, weight=1)

                        holder = tk.Frame(stripe, bg=row_bg, highlightthickness=0, bd=0)
                        holder.pack(padx=24, pady=(12, 12), anchor="center")

                        for c, book in enumerate(row_books):
                            cell = _add_book_tile(holder, book, row_bg, rows_sorted)
                            cell.grid(row=0, column=c, padx=(pad_x // 2, pad_x // 2), sticky="n")

                        r += 1

                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox("all"))
                return

            # --- NORMAL GRID (your existing behavior) ---
            row_chunks = [rows_sorted[i:i + cols] for i in range(0, len(rows_sorted), cols)]

            for r, row_books in enumerate(row_chunks):
                row_bg = SHARED_TABLE_ALTROW_BG_COLOR if (r % 2 == 0) else panel_bg

                stripe = tk.Frame(scroll_frame, bg=row_bg, highlightthickness=0, bd=0)
                stripe.grid(row=r, column=0, sticky="nsew", padx=0, pady=(0 if r == 0 else pad_y, 0))
                stripe.grid_columnconfigure(0, weight=1)

                holder = tk.Frame(stripe, bg=row_bg, highlightthickness=0, bd=0)
                holder.pack(padx=24, pady=(12, 12), anchor="center")

                for c, book in enumerate(row_books):
                    cell = _add_book_tile(holder, book, row_bg, rows_sorted)
                    cell.grid(row=0, column=c, padx=(pad_x // 2, pad_x // 2), sticky="n")
        def render_list_view(mode: str):
            _force_canvas_window_width()
            clear_scroll_contents()

            # Get secondary sort from the variable
            secondary = secondary_sort_var.get() if secondary_sort_var else ""
            reverse = secondary_sort_reverse_var.get() if secondary_sort_reverse_var else False
            rows_sorted = _sorted_rows(mode, secondary, reverse)

            total_w = max(canvas.winfo_width(), 1)
            total_w = max(total_w - 24, 1)

            header_font = (SHARED_FONT_TABLE, 18)
            row_font = (SHARED_FONT_TABLE, 18)

            if is_collection:
                editable = bool(getattr(self, "_mark_read_mode", False))
                cb_w = 70  # always present

                usable_w = max(total_w - cb_w, 1)

                title_w = max(int(usable_w * 0.46), 300)
                author_w = max(int(usable_w * 0.24), 180)
                genre_w = max(int(usable_w * 0.16), 140)
                updated_w = max(usable_w - title_w - author_w - genre_w, 140)

                header = tk.Frame(scroll_frame, bg=SHARED_SUBHEADER_BG_COLOR, highlightthickness=0, bd=0)
                header.grid(row=0, column=0, sticky="we")

                col_widths = (cb_w, title_w, author_w, genre_w, updated_w)
                for i, w in enumerate(col_widths):
                    header.grid_columnconfigure(i, minsize=w)

                # Define header columns with their sort field names
                header_cols = [
                    ("Read", 0, "Read"),
                    ("Title", 1, "Title"),
                    ("Author", 2, "Author"),
                    ("Genre", 3, "Genre"),
                    ("Updated", 4, "Updated"),
                ]

                for text, col_idx, sort_field in header_cols:
                    # Show indicator if this is the secondary sort
                    display_text = text
                    if secondary and secondary.lower() == sort_field.lower():
                        # Show arrow direction based on reverse state
                        arrow = "▲" if reverse else "▼"
                        display_text = f"{arrow} {text}"

                    hdr_lbl = tk.Label(header, text=display_text, bg=SHARED_SUBHEADER_BG_COLOR, fg=SHARED_SUBHEADER_TEXT_COLOR,
                                       font=header_font, anchor="w", padx=12, pady=10, cursor="hand2")
                    hdr_lbl.grid(row=0, column=col_idx, sticky="we")

                    def _on_header_click(e=None, field=sort_field):
                        # Toggle reverse if clicking same column, otherwise set new column
                        current = secondary_sort_var.get() if secondary_sort_var else ""
                        if current.lower() == field.lower():
                            # Toggle reverse direction
                            current_reverse = secondary_sort_reverse_var.get() if secondary_sort_reverse_var else False
                            secondary_sort_reverse_var.set(not current_reverse)
                        else:
                            # New column - start with A-Z (not reversed)
                            secondary_sort_var.set(field)
                            secondary_sort_reverse_var.set(False)
                        render_content()

                    hdr_lbl.bind("<Button-1>", _on_header_click)

                for idx, book in enumerate(rows_sorted, start=1):
                    row_bg = SHARED_TABLE_ALTROW_BG_COLOR if idx % 2 == 0 else SHARED_TABLE_BG_COLOR
                    row = tk.Frame(scroll_frame, bg=row_bg, highlightthickness=0, bd=0)
                    row.grid(row=idx, column=0, sticky="we")
                    row.grid_columnconfigure(0, minsize=cb_w)
                    row.grid_columnconfigure(1, minsize=title_w)
                    row.grid_columnconfigure(2, minsize=author_w)
                    row.grid_columnconfigure(3, minsize=genre_w)
                    row.grid_columnconfigure(4, minsize=updated_w)

                    # ✅ ALWAYS configure 5 columns in collection list view
                    for i, w in enumerate((cb_w, title_w, author_w, genre_w, updated_w)):
                        row.grid_columnconfigure(i, minsize=w)

                    author, title, _year = self._get_display_fields(book)
                    genre_txt = _norm_genre(book.get("genre")).title()
                    updated_txt = self._ts_to_short_date(_collection_updated_ts(book))

                    title_txt = self._ellipsize_px(title, row_font, title_w - 24)
                    author_txt = self._ellipsize_px(author, row_font, author_w - 24)
                    genre_txt = self._ellipsize_px(genre_txt, row_font, genre_w - 24)
                    updated_txt = self._ellipsize_px(updated_txt, row_font, updated_w - 24)

                    col_name = (collection_name or self._current_open_collection_name() or "").strip()

                    # ✅ load persisted marks once per collection
                    if col_name and col_name not in self._collection_read_marks:
                        try:
                            self._collection_read_marks[col_name] = set(self.data.get_collection_read_marks(col_name))
                        except Exception:
                            self._collection_read_marks[col_name] = set()

                    key = self._book_key(book)
                    var = tk.IntVar(
                        value=1 if (col_name and key in self._collection_read_marks.get(col_name, set())) else 0)

                    def _save_mark(k=key, v=var, cn=col_name):
                        # editable toggle only controls whether user can change it
                        if not bool(getattr(self, "_mark_read_mode", False)):
                            return
                        if not cn:
                            return

                        is_read = bool(v.get())
                        if is_read:
                            self._collection_read_marks.setdefault(cn, set()).add(k)
                        else:
                            self._collection_read_marks.setdefault(cn, set()).discard(k)

                        # ✅ persist
                        try:
                            self.data.set_collection_read(cn, k, is_read)
                        except Exception:
                            pass

                    cb = tk.Checkbutton(
                        row,
                        variable=var,
                        command=_save_mark,
                        state=("normal" if bool(getattr(self, "_mark_read_mode", False)) else "disabled"),
                        bg=row_bg,
                        activebackground=row_bg,
                        highlightthickness=0,
                        bd=0,
                        takefocus=False,
                    )
                    cb.grid(row=0, column=0, sticky="w", padx=12)
                    self.active_widgets.append(cb)

                    cells = [
                        tk.Label(row, text=title_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                                 anchor="w", padx=12, pady=8, cursor="hand2"),
                        tk.Label(row, text=author_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                                 anchor="w", padx=12, pady=8, cursor="hand2"),
                        tk.Label(row, text=genre_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                                 anchor="w", padx=12, pady=8, cursor="hand2"),
                        tk.Label(row, text=updated_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                                 anchor="w", padx=12, pady=8, cursor="hand2"),
                    ]

                    for c, lbl in enumerate(cells):
                        lbl.grid(row=0, column=1 + c, sticky="we")  # ✅ offset by 1 because col0 is Read
                        lbl.bind("<Button-1>",
                                 lambda e, b=book, rows=rows_sorted: self._open_book_from_list(b, rows, context_label))
                        self.active_widgets.append(lbl)

                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox("all"))
                return

            # --- compute column widths (pixels) from the visible canvas width ---
            total_w = max(canvas.winfo_width(), 1)

            # leave a little breathing room so text doesn't kiss the scrollbar
            total_w = max(total_w - 24, 1)

            # Title | Author | Year
            title_w = max(int(total_w * 0.62), 320)
            author_w = max(int(total_w * 0.28), 200)
            year_w = max(total_w - title_w - author_w, 90)

            header_font = (SHARED_FONT_TABLE, 18)
            row_font = (SHARED_FONT_TABLE, 18)

            # --- header row (fixed widths so it aligns with data) ---
            header = tk.Frame(scroll_frame, bg=SHARED_SUBHEADER_BG_COLOR, highlightthickness=0, bd=0)
            header.grid(row=0, column=0, sticky="we")

            for i, w in enumerate((title_w, author_w, year_w)):
                header.grid_columnconfigure(i, minsize=w)

            # Define header columns with their sort field names
            header_cols = [
                ("Title", 0, "Title"),
                ("Author", 1, "Author"),
                ("Year", 2, "Year"),
            ]

            secondary = secondary_sort_var.get() if secondary_sort_var else ""
            reverse = secondary_sort_reverse_var.get() if secondary_sort_reverse_var else False

            for text, col_idx, sort_field in header_cols:
                # Show indicator if this is the secondary sort
                display_text = text
                if secondary and secondary.lower() == sort_field.lower():
                    # Show arrow direction based on reverse state
                    arrow = "▲" if reverse else "▼"
                    display_text = f"{arrow} {text}"

                hdr_lbl = tk.Label(header, text=display_text, bg=SHARED_SUBHEADER_BG_COLOR, fg=SHARED_SUBHEADER_TEXT_COLOR,
                                   font=header_font, anchor="w", padx=12, pady=10, cursor="hand2")
                hdr_lbl.grid(row=0, column=col_idx, sticky="we")

                def _on_header_click(e=None, field=sort_field):
                    # Toggle reverse if clicking same column, otherwise set new column
                    current = secondary_sort_var.get() if secondary_sort_var else ""
                    if current.lower() == field.lower():
                        # Toggle reverse direction
                        current_reverse = secondary_sort_reverse_var.get() if secondary_sort_reverse_var else False
                        secondary_sort_reverse_var.set(not current_reverse)
                    else:
                        # New column - start with A-Z (not reversed)
                        secondary_sort_var.set(field)
                        secondary_sort_reverse_var.set(False)
                    render_content()

                hdr_lbl.bind("<Button-1>", _on_header_click)

            # --- data rows ---
            for idx, book in enumerate(rows_sorted, start=1):
                row_bg = SHARED_TABLE_ALTROW_BG_COLOR if idx % 2 == 0 else panel_bg

                row = tk.Frame(scroll_frame, bg=row_bg, highlightthickness=0, bd=0)
                row.grid(row=idx, column=0, sticky="we")


                for i, w in enumerate((title_w, author_w, year_w)):
                    row.grid_columnconfigure(i, minsize=w)

                author, title, year = self._get_display_fields(book)

                # Ellipsize to fit pixel widths (minus padding)
                title_txt = self._ellipsize_px(title, row_font, title_w - 24)
                author_txt = self._ellipsize_px(author, row_font, author_w - 24)
                year_txt = self._ellipsize_px(year, row_font, year_w - 24)

                cells = [
                    tk.Label(row, text=title_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                             anchor="w", padx=12, pady=8, cursor="hand2"),
                    tk.Label(row, text=author_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                             anchor="w", padx=12, pady=8, cursor="hand2"),
                    tk.Label(row, text=year_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                             anchor="w", padx=12, pady=8, cursor="hand2"),
                ]

                cells[0].grid(row=0, column=0, sticky="we")
                cells[1].grid(row=0, column=1, sticky="we")
                cells[2].grid(row=0, column=2, sticky="we")

                for lbl in cells:
                    lbl.bind(
                        "<Button-1>",
                        lambda e, b=book, rows=rows_sorted: self._open_book_from_list(b, rows, context_label),
                    )
                    self.active_widgets.append(lbl)

            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        def render_content():
            mode = sort_var.get()
            view = view_var.get()
            if view == "list":
                render_list_view(mode)
            else:
                render_grid_view(mode)

        # --- debounced list rerender (prevents jitter from tiny width oscillations) ---
        _last_list_w = {"w": 0}

        def _on_list_resize(event):
            if view_var.get() != "list":
                return

            w = int(getattr(event, "width", 0) or canvas.winfo_width())
            # ignore tiny width changes (often scrollbar/layout micro-adjustments)
            if abs(w - _last_list_w["w"]) < 8:
                return
            _last_list_w["w"] = w

            after_id = getattr(self, "_list_resize_after", None)
            if after_id:
                try:
                    self.after_cancel(after_id)
                except Exception:
                    pass
            self._list_resize_after = self.after(90, render_content)

        canvas.bind("<Configure>", _on_list_resize)

        # --- (re)build radios inside the provided view_btns container ---
        for child in view_btns.winfo_children():
            child.destroy()

        grid_rb = self._make_bubble_radio(
            view_btns, text="Grid", variable=view_var, value="grid", command=render_content, bg=SHARED_MAINHEADER_BG_COLOR)
        list_rb = self._make_bubble_radio(
            view_btns, text="List", variable=view_var, value="list", command=render_content, bg=SHARED_MAINHEADER_BG_COLOR)

        self.active_widgets.extend([grid_rb, list_rb])

        # Sort changes -> rerender
        sort_var.trace_add("write", lambda *_: render_content())

        # Secondary sort changes -> rerender (if provided)
        if secondary_sort_var:
            secondary_sort_var.trace_add("write", lambda *_: render_content())

        # Initial render
        render_content()
    def _make_books_browser_card(self,*,panel_bg: str,header_h: int, context_label: str,books: list[dict],cols: int = 5,
            default_view: str = "grid",default_sort: str = "Title",sort_values: tuple[str, ...] = ("Title", "Author", "Year"),
                                 is_collection: bool = False,collection_name: str | None = None,):

        container, canvas, scroll_frame = self._make_scroll_container(
            bg=SHARED_TABLE_BG_COLOR,
            relwidth=0.88,
            relheight=0.68,
            top_inset=header_h,)

        header = tk.Frame(container, bg=SHARED_MAINHEADER_BG_COLOR, height=header_h, highlightthickness=0, bd=0)
        header.place(x=0, y=0, relwidth=1.0, height=header_h)
        header.pack_propagate(False)
        self.active_widgets.append(header)

        sort_var, view_var, view_btns, secondary_sort_var, secondary_sort_reverse_var = self._make_sort_and_view_controls(
            header,
            bg=SHARED_MAINHEADER_BG_COLOR,
            pad_x=18,
            pad_y=10,
            default_view=default_view,
            default_sort=default_sort,
            sort_values=sort_values
        )

        if not books:
            tk.Label(
                scroll_frame,
                text="No books found.",
                font=(SHARED_FONT_CUSTOM, 22),
                bg=panel_bg,
                fg=SHARED_SCROLLROW_TEXT_COLOR,
                pady=30,
            ).pack()
            return container, canvas, scroll_frame, sort_var, view_var, secondary_sort_var, secondary_sort_reverse_var

        self._render_books_grid_or_list(
            canvas=canvas,
            scroll_frame=scroll_frame,
            books=books,
            sort_var=sort_var,
            view_var=view_var,
            view_btns=view_btns,
            context_label=context_label,
            panel_bg=panel_bg,
            cols=cols,
            is_collection=is_collection,
            collection_name=collection_name,
            secondary_sort_var=secondary_sort_var,
            secondary_sort_reverse_var=secondary_sort_reverse_var,
        )

        return container, canvas, scroll_frame, sort_var, view_var, secondary_sort_var, secondary_sort_reverse_var
    def _ellipsize_px(self, text: str, font, max_px: int) -> str:
        """Return text truncated to fit max_px pixels, with … when needed."""
        text = (text or "").strip()
        if max_px <= 10:
            return "…"

        f = tkfont.Font(font=font)
        if f.measure(text) <= max_px:
            return text

        ell = "…"
        ell_w = f.measure(ell)
        if ell_w >= max_px:
            return ell

        lo, hi = 0, len(text)
        # binary search best cut
        while lo < hi:
            mid = (lo + hi) // 2
            cand = text[:mid].rstrip() + ell
            if f.measure(cand) <= max_px:
                lo = mid + 1
            else:
                hi = mid

        cut = max(0, lo - 1)
        return text[:cut].rstrip() + ell
    def _get_collection_record(self, collection_name: str) -> dict | None:
        """Return the collection record dict by name (case-insensitive)."""
        target = (collection_name or "").strip().lower()
        if not target:
            return None
        try:
            for rec in (self.data.list_collections() or []):
                name = (rec.get("name") or "").strip().lower()
                if name == target:
                    return rec
        except Exception:
            return None
        return None
    def _collection_book_ids(self, rec: dict) -> list[str]:
        """
        Return a normalized list of book id strings from a collection record.
        Handles: list[str], list[int], comma-strings, and accidental dict items.
        """
        ids = rec.get("book_ids") or rec.get("ids") or []

        # sometimes data ends up as a single comma-separated string
        if isinstance(ids, str):
            ids = [p.strip() for p in ids.split(",") if p.strip()]

        out: list[str] = []

        def _coerce_one(x) -> str | None:
            if x is None:
                return None

            # If an item is accidentally a dict (common when something saves whole objects)
            if isinstance(x, dict):
                for fld in ("book_id", "id", "isbn13", "isbn_13", "isbn10", "isbn_10", "isbn", "title"):
                    v = x.get(fld)
                    if v is None:
                        continue
                    if isinstance(v, (int, float)):
                        v = str(int(v))
                    v = str(v).strip()
                    if v:
                        return v
                return None

            # numbers -> string
            if isinstance(x, (int, float)):
                try:
                    return str(int(x))
                except Exception:
                    return str(x).strip() or None

            s = str(x).strip()
            return s or None

        for x in ids:
            s = _coerce_one(x)
            if s:
                out.append(s)

        return out
    def _collection_books(self, col_rec: dict) -> list[dict]:
        """Return actual book dicts for a collection record's book_ids (preserve order)."""

        def _digits(s: str) -> str:
            return re.sub(r"\D+", "", s or "")

        def _canon(s: str) -> str:
            return self._norm(str(s or ""))

        all_books = self._all_books()  # must return real book dicts

        # Build a multi-key index so collections saved under older key styles still resolve.
        by_key: dict[str, dict] = {}

        for b in all_books:
            candidates: set[str] = set()

            for fld in ("book_id", "id", "isbn13", "isbn_13", "isbn10", "isbn_10", "isbn", "title"):
                v = b.get(fld)
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    v = str(int(v))
                v = str(v).strip()
                if not v:
                    continue

                candidates.add(v)
                candidates.add(_canon(v))

                d = _digits(v)
                if d:
                    candidates.add(d)

            for k in candidates:
                if k and k not in by_key:
                    by_key[k] = b

        # normalize ids coming from the collection record
        ids = self._collection_book_ids(col_rec)

        out: list[dict] = []
        seen: set[str] = set()

        for raw in ids:
            probes = [raw, _canon(raw), _digits(raw)]
            found = None
            for p in probes:
                if p and p in by_key:
                    found = by_key[p]
                    break

            if found:
                stable = self._book_key(found)
                if stable not in seen:
                    out.append(found)
                    seen.add(stable)

        return out
    def _books_by_ids(self, ids: list[str]) -> list[dict]:
        """
        Resolve book dicts for a list of ids that may be:
        - book_id / id
        - isbn13 / isbn10 / isbn (with or without dashes/spaces)
        - normalized text versions
        - (last resort) title

        This matches what your builder saves via _book_key().
        """
        if not ids:
            return []

        def _canon(s: str) -> str:
            return self._norm(str(s or ""))

        def _digits(s: str) -> str:
            return re.sub(r"\D+", "", str(s or ""))

        # normalize incoming ids
        wanted: list[str] = []
        for raw in ids:
            if raw is None:
                continue
            if isinstance(raw, (int, float)):
                raw = str(int(raw))
            raw = str(raw).strip()
            if raw:
                wanted.append(raw)

        if not wanted:
            return []

        # Build a multi-key index across ALL books
        by_key: dict[str, dict] = {}

        for b in self._all_books():
            candidates: set[str] = set()

            # include your stable key too
            try:
                candidates.add(str(self._book_key(b)).strip())
            except Exception:
                pass

            for fld in ("book_id", "id", "isbn13", "isbn_13", "isbn10", "isbn_10", "isbn", "title"):
                v = b.get(fld)
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    v = str(int(v))
                v = str(v).strip()
                if not v:
                    continue

                candidates.add(v)
                candidates.add(_canon(v))

                d = _digits(v)
                if d:
                    candidates.add(d)

            for k in candidates:
                if k and k not in by_key:
                    by_key[k] = b

        # Resolve in saved order, dedupe by stable book key
        out: list[dict] = []
        seen: set[str] = set()

        for raw in wanted:
            probes = [raw, _canon(raw), _digits(raw)]
            found = None
            for p in probes:
                if p and p in by_key:
                    found = by_key[p]
                    break

            if found:
                stable = self._book_key(found)
                if stable not in seen:
                    out.append(found)
                    seen.add(stable)

        return out
    def _ellipsize(self, s: str, max_chars: int = 44) -> str:
        s = (s or "").strip()
        if len(s) <= max_chars:
            return s
        return s[: max_chars - 1].rstrip() + "…"
    def _render_open_collection_results(self,collection_name: str,host_scroll_frame: tk.Frame,
            books: list[dict],sort_mode: str,view_mode: str,cols: int = 5,) -> None:
        """
        Clears + re-renders the scrollable results area for the open collection page ONLY.
        - sort_mode: "genre" or "last_updated"
        - view_mode: "grid" or "list"
        """
        # clear previous children in scroll content
        for w in host_scroll_frame.winfo_children():
            w.destroy()

        sorted_books = self.data.sort_collection_books(collection_name, books, sort_mode)

        if view_mode == "list":
            # LIST VIEW (Genre must be a column ONLY HERE)
            # Build your list/table rows however you already do it.
            # The key change: include a Genre column + use collection timestamp if you want.
            self._render_collection_list_view(host_scroll_frame, sorted_books)
            return

        # GRID VIEW
        if sort_mode == "genre":
            grouped = self.data.group_books_by_genre(sorted_books)

            # grid config
            for c in range(cols):
                host_scroll_frame.grid_columnconfigure(c, weight=1)

            r = 0
            for genre, group_books in grouped:
                header = self._make_genre_header_row(host_scroll_frame, genre, cols, bg=OPENCOLL_HEADER_BG_COLOR, fg=OPENCOLL_HEADER_FG_COLOR)
                header.grid(row=r, column=0, columnspan=cols, sticky="ew")
                r += 1

                # now render the book cards in a grid
                c = 0
                for b in group_books:
                    card = self._make_collection_book_card(host_scroll_frame,
                                                           b)  # <-- you implement/point to your existing card builder
                    card.grid(row=r, column=c, padx=10, pady=10, sticky="n")
                    c += 1
                    if c >= cols:
                        c = 0
                        r += 1
                if c != 0:
                    r += 1
            return

        # normal GRID VIEW (not grouped)
        for c in range(cols):
            host_scroll_frame.grid_columnconfigure(c, weight=1)

        r = 0
        c = 0
        for b in sorted_books:
            card = self._make_collection_book_card(host_scroll_frame, b)
            card.grid(row=r, column=c, padx=10, pady=10, sticky="n")
            c += 1
            if c >= cols:
                c = 0
                r += 1
    def _make_collection_book_card(self, parent: tk.Frame, book: dict) -> tk.Frame:
        """
        Replace this body with your existing card creation if you already have it.
        Keep it collection-page-specific if you want (extra buttons, edit details, etc.).
        """
        card = tk.Frame(parent, width=200, height=240, bg="", highlightthickness=0, bd=0)
        card.pack_propagate(False)

        tk.Label(card, text=book.get("title", ""), bg="", fg=SHARED_SUBHEADER_BG_COLOR, wraplength=180, justify="left").pack(anchor="w")
        tk.Label(card, text=book.get("author", ""), bg="", fg=THEME_COLOR2).pack(anchor="w")

        return card

    # ---------- NAV ----------
    def _set_menu_button_visible(self, visible: bool) -> None:
        """Show/hide the side-menu button (canvas image item)."""
        item = getattr(self, "_menu_btn_item", None)
        if not item:
            return
        try:
            # Only configure if the item still exists on the canvas
            if self.canvas.type(item):
                self.canvas.itemconfigure(item, state=("normal" if visible else "hidden"))
                if visible:
                    self._position_menu_button()
        except Exception:
            pass

    def go_home(self):
        # ✅ FIXED: Clear history when going home so we start fresh
        self._nav_history.clear()
        self._nav_suppress_record = True
        self.show_main_page()
    def set_page(self, page_name: str, **payload):
        """Single source of truth for navigation state."""
        prev_page = getattr(self, "current_page", None)
        prev_payload = getattr(self, "page_payload", {}) or {}

        # Hide side menu button ONLY on Settings page
        self._set_menu_button_visible(page_name != "settings")

        # If the side menu is open and we navigate to Settings, close it
        if page_name == "settings" and getattr(self, "_side_menu_open", False):
            self.close_side_menu()

        # Record history unless we are doing a "back" jump or a refresh rebuild.
        if not getattr(self, "_nav_suppress_record", False):
            if prev_page is not None:
                same_page = (prev_page == page_name)
                payload_changed = (dict(prev_payload) != dict(payload))

                # ✅ FIXED: Record navigation properly
                # - Always record when moving to a different page
                # - For search_results and view_all pages, also record when filter changes
                should_record = False

                if not same_page:
                    # Different page = always record
                    should_record = True
                elif same_page and page_name == "search_results" and payload_changed:
                    # Same page (search_results) but different query = record it
                    should_record = True
                elif same_page and page_name == "view_all" and payload_changed:
                    # Same page (view_all) but different letter_filter = record it
                    should_record = True

                if should_record:
                    self._nav_history.append((prev_page, dict(prev_payload)))
                    # keep it from growing forever
                    if len(self._nav_history) > 60:
                        self._nav_history = self._nav_history[-60:]

        # reset the suppress flag after each navigation
        self._nav_suppress_record = False

        self.current_page = page_name
        self.page_payload = dict(payload)
    def _open_book_from_list(self, book: dict, rows: list[dict] | None, query_label: str = ""):
        # rows may be None (fallback)
        self.last_search_results = list(rows) if rows is not None else None
        self.last_search_query = query_label or ""
        # Manually push a breadcrumb for Back, regardless of suppression flags
        prev_page = getattr(self, 'current_page', None)
        prev_payload = getattr(self, 'page_payload', {}) or {}
        if prev_page is not None:
            self._nav_history.append((prev_page, dict(prev_payload)))
            if len(self._nav_history) > 60:
                self._nav_history = self._nav_history[-60:]

        # Preserve origin when coming from a collection card/list
        origin = {}
        if isinstance(query_label, str) and query_label.startswith('Collection: '):
            origin_name = query_label[len('Collection: '):].strip()
            if origin_name:
                origin = {'from': 'open_collection', 'collection_name': origin_name}
        b = dict(book)
        if origin and '_origin' not in b:
            b['_origin'] = origin
        self.show_book_detail(b)
    def _nav_go(self, page: str, payload: dict | None = None):
        """Navigate to a page name using your existing page functions."""
        payload = payload or {}

        if page == "browse_genres":
            self.show_browse_genres_page(payload.get("tab", "fiction"))
        elif page == "genre_page":
            self.show_genre_page(payload.get("genre", ""))
        elif page == "tag_page":
            self.show_tag_page(payload.get("tag", ""))
        elif page == "view_all":
            letter_filter = payload.get("letter_filter")
            self.show_all_books_page(letter_filter)
        elif page == "settings":
            self.show_settings_page()
        elif page == "collections":
            self.show_collections_page()
        elif page == "open_collection":
            # Navigate back to an open collection page
            name = payload.get("name", "")
            letter_filter = payload.get("letter_filter")
            filter_field = payload.get("filter_field", "Title")
            if name:
                self.show_open_collection_page(name, letter_filter=letter_filter, filter_field=filter_field)
            else:
                self.show_collections_page()
        elif page == "search_results":
            # Use query from payload if available, otherwise fall back to saved state
            query = payload.get("query", "")
            if query:
                self.perform_search(query)
            elif self.last_search_results is not None:
                self.show_search_results(self.last_search_results, original_query=self.last_search_query)
            else:
                self.show_all_books_page()
        elif page == "book_detail":
            book = payload.get("book")
            if book:
                self.show_book_detail(book)
            else:
                self.show_main_page()
        elif page == "build_collection":
            # Navigate back to build collection page
            prefill_name = payload.get("prefill_name")
            prefill_ids = payload.get("prefill_ids", [])
            edit_id = payload.get("edit_collection_id")
            self.show_build_collection_page(prefill_name=prefill_name, prefill_ids=prefill_ids, edit_collection_id=edit_id)
        else:
            self.show_main_page()
    def go_back(self):

        if not self._nav_history:
            # Fallback: Book Info opened from Collection → return to that collection
            if getattr(self, 'current_page', '') == 'book_detail':
                payload_book = (getattr(self, 'page_payload', {}) or {}).get('book', {}) or {}
                origin = payload_book.get('_origin') or (getattr(self, '_current_book_detail', {}) or {}).get('_origin')
                if isinstance(origin, dict) and origin.get('from') == 'open_collection':
                    name = (origin.get('collection_name') or '').strip()
                    if name:
                        self._nav_suppress_record = True
                        self.show_open_collection_page(name)
                        return
            self.go_home()
            return
        prev_page, prev_payload = self._nav_history.pop()
        # Prevent destination page from re-recording itself
        self._nav_suppress_record = True
        self._nav_go(prev_page, prev_payload)
    def mount_left_nav(self):
        """
        Enforces your global rule:
        - Not main: show Home
        - Back appears only after the 2nd navigation away from Home (handled inside make_left_nav_stack)
        - Back is always stacked immediately above Home
        """
        if getattr(self, "current_page", "") == "main":
            return

        # IMPORTANT: Do NOT manually add a Back button here.
        # and ensures Back is placed directly above Home.
        self.make_left_nav_stack(
            home_text="Home",
            home_cmd=self.go_home,
        )

    # =========================
    # Collections UI
    # =========================
    def _collections_all(self) -> list[dict]:
        """Saved collections (LibraryData) + in-memory collections + optional samples."""
        rows: list[dict] = []

        # 1) from LibraryData (if available)
        try:
            saved = self.data.list_collections()
            if isinstance(saved, list):
                rows.extend(saved)
        except Exception:
            pass

        # 2) from in-memory dict (your current builder saves here)
        try:
            now = time.time()
            mem = []
            for name, ids in (self.collections or {}).items():
                meta = getattr(self, "_collections_meta", {}).get(name, {})
                created = float(meta.get("created_at") or 0.0) or 0.0
                updated = float(meta.get("updated_at") or 0.0) or created or 0.0
                mem.append({
                    "name": name,
                    "book_ids": list(ids or []),
                    "created_at": created,
                    "updated_at": updated,
                })

            # avoid duplicate names if LibraryData already returned it
            existing = {(c.get("name") or "").strip().lower() for c in rows}
            for c in mem:
                if (c.get("name") or "").strip().lower() not in existing:
                    rows.append(c)
        except Exception:
            pass

        # 3) optional sample collections
        sample = getattr(self, "sample_collections", None)
        if isinstance(sample, list):
            rows.extend(sample)

        return rows
    def _find_collection_record(self, name: str) -> dict | None:
        """Find a collection record by name (case/space-insensitive) from _collections_all()."""
        target = self._norm(name)
        for c in self._collections_all():
            n = (c.get("name") or "").strip()
            if self._norm(n) == target:
                return c
        return None
    def _open_book_from_tile(self, b: dict):
        """Best-effort open book detail using whatever method your app already has."""
        if hasattr(self, "show_book_info_page"):
            return self.show_book_info_page(b)
        if hasattr(self, "show_book_info"):
            return self.show_book_info(b)
        # fallback
        messagebox.showinfo("Book", self._book_label(b))
    def show_open_collection_page(self, collection_name: str, letter_filter: str | None = None, filter_field: str = "Title"):
        self.set_page("open_collection", name=collection_name, letter_filter=letter_filter, filter_field=filter_field)
        self.clear_page()
        self.set_background(OPEN_COLLECTION_BG_IMG)
        try:
            self._page_img_refs.clear()
        except Exception:
            pass

        # ---- title ----
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=56, weight="bold")

        self.make_canvas_text(collection_name, relx=0.5, rely=0.08, font=title_font)

        # ---- load collection record ----
        rec = self._get_collection_record(collection_name) or self._find_collection_record(collection_name)
        if not rec:
            messagebox.showerror("Not found", f'Collection "{collection_name}" was not found.')
            self.show_collections_page()
            return

        # ---- resolve books ----
        try:
            all_books = self._collection_books(rec)
        except Exception:
            all_books = self._books_by_ids(self._collection_book_ids(rec))

        # Apply letter filter if set
        if letter_filter:
            books = [b for b in all_books if self._get_filter_first_char(b, filter_field) == letter_filter]
        else:
            books = all_books

        # Build context label
        context_label = f'Collection: {collection_name}'
        if letter_filter:
            field_display = filter_field
            if filter_field == "Author (Last Name)":
                field_display = "Author"
            if letter_filter == "#":
                context_label = f"{context_label} ({field_display}: 0-9)"
            elif letter_filter == "~":
                context_label = f"{context_label} ({field_display}: Symbols)"
            else:
                context_label = f"{context_label} ({field_display}: {letter_filter})"

        # ---- left nav stack ----
        # Add "Done" button above Back when in mark-read mode
        if getattr(self, "_mark_read_mode", False):
            def _exit_mark_read_mode():
                self._mark_read_mode = False
                self._mark_read_force_list = False
                self.show_open_collection_page(collection_name)

            self.make_left_nav_stack(
                home_text="Home",
                home_cmd=self.go_home,
                extra_buttons=[("Done", _exit_mark_read_mode)],
            )
        else:
            self.mount_left_nav()

        # Alphabet filter bar callback
        def on_filter_change(new_letter: str | None, new_field: str):
            self.show_open_collection_page(
                collection_name=collection_name,
                letter_filter=new_letter,
                filter_field=new_field,
            )

        # Create alphabet bar - starts at rely=0.145
        alphabet_bar_rely = 0.145
        self._make_alphabet_filter_bar(
            books=all_books,
            filter_field=filter_field,
            letter_filter=letter_filter,
            on_filter_change=on_filter_change,
            show_filter_dropdown=True,
            rely=alphabet_bar_rely,
        )

        # ---- single browser card (ONE UI) ----
        # Force list view if mark-read mode is active (checkboxes only in list view)
        effective_default_view = "grid"
        if getattr(self, "_mark_read_force_list", False) and getattr(self, "_mark_read_mode", False):
            effective_default_view = "list"

        container, canvas, scroll_frame, sort_var, view_var, secondary_sort_var, secondary_sort_reverse_var = self._make_books_browser_card(
            panel_bg=SHARED_TABLE_BG_COLOR,
            header_h=60,
            context_label=context_label,
            books=books,
            cols=5,
            default_view=effective_default_view,
            default_sort="Last Updated",
            # 👇 allow collection-only sort options
            sort_values=("Title", "Author", "Year", "Genre", "Last Updated"),
            # 👇 pass collection_name so renderer can use timestamps safely
            collection_name=collection_name,
            is_collection=True,
        )

        # Position container so its top aligns exactly with bottom of alphabet bar
        container.place_configure(
            relx=0.50,
            rely=alphabet_bar_rely,
            y=36,  # Offset by alphabet bar height
            relwidth=0.88,
            relheight=0.60,
            anchor="n",
        )
    def _ts_to_short_date(self, ts: float) -> str:
        try:
            ts = float(ts or 0.0)
            if ts <= 0:
                return ""
            return time.strftime("%Y-%m-%d", time.localtime(ts))
        except Exception:
            return ""
    def _sort_collections(self, rows: list[dict], mode: str) -> list[dict]:
        mode = (mode or "").strip()
        if mode == "Name":
            return sorted(rows, key=lambda c: (c.get("name") or "").strip().lower())
        if mode == "Date Created":
            return sorted(rows, key=lambda c: float(c.get("created_at") or 0.0), reverse=True)
        # Last Updated (default): newest first
        return sorted(rows, key=lambda c: float(c.get("updated_at") or 0.0), reverse=True)
    def _render_collections_grid_or_list(self, *,canvas: tk.Canvas,scroll_frame: tk.Frame,collections: list[dict],sort_var: tk.StringVar,
            view_var: tk.StringVar,view_btns: tk.Widget,panel_bg: str,cols: int = 5,
            sort_reverse_var: tk.BooleanVar | None = None):
        """Matches the Search Results feel: pinned header + grid/list with stripes.
        Clickable column headers for sorting in list view."""

        tile = 130  # blank square size
        pad_x, pad_y = 24, 18

        # Create reverse var if not provided
        if sort_reverse_var is None:
            sort_reverse_var = tk.BooleanVar(value=False)

        def _force_canvas_window_width():
            wid = getattr(canvas, "_inner_window_id", None)
            if wid is None:
                return
            try:
                canvas.itemconfig(wid, width=max(canvas.winfo_width(), 1))
            except Exception:
                pass
            try:
                scroll_frame.configure(width=max(canvas.winfo_width(), 1))
            except Exception:
                pass

        def clear_scroll_contents():
            for child in scroll_frame.winfo_children():
                child.destroy()

        def _sort_collections_with_reverse(rows: list[dict], mode: str, reverse: bool) -> list[dict]:
            mode = (mode or "").strip()
            if mode == "Name":
                sorted_rows = sorted(rows, key=lambda c: (c.get("name") or "").strip().lower())
            elif mode == "Books":
                sorted_rows = sorted(rows, key=lambda c: len(c.get("book_ids") or []), reverse=True)
            elif mode == "Created":
                sorted_rows = sorted(rows, key=lambda c: float(c.get("created_at") or 0.0), reverse=True)
            else:  # Last Updated (default)
                sorted_rows = sorted(rows, key=lambda c: float(c.get("updated_at") or 0.0), reverse=True)
            
            if reverse:
                sorted_rows = list(reversed(sorted_rows))
            return sorted_rows

        def render_grid_view(mode: str, reverse: bool = False):
            _force_canvas_window_width()
            clear_scroll_contents()

            rows_sorted = _sort_collections_with_reverse(collections, mode, reverse)
            canvas.update_idletasks()
            avail_w = max(canvas.winfo_width(), 1)

            # account for stripe/holder padding you apply
            side_padding = 24 * 2  # holder.pack(padx=24)
            cell_w = tile + pad_x  # approx footprint per cell
            dynamic_cols = max(1, (avail_w - side_padding) // max(cell_w, 1))

            # respect the user-provided cols as a maximum
            use_cols = max(1, min(int(cols), int(dynamic_cols)))

            chunks = [rows_sorted[i:i + cols] for i in range(0, len(rows_sorted), cols)]

            for r, row_cols in enumerate(chunks):
                row_bg = SHARED_TABLE_ALTROW_BG_COLOR if (r % 2 == 0) else panel_bg

                stripe = tk.Frame(scroll_frame, bg=row_bg, highlightthickness=0, bd=0)
                stripe.grid(row=r, column=0, sticky="nsew", padx=0, pady=(0 if r == 0 else pad_y, 0))
                stripe.grid_columnconfigure(0, weight=1)

                holder = tk.Frame(stripe, bg=row_bg, highlightthickness=0, bd=0)
                holder.pack(fill="x", expand=True, padx=24, pady=(12, 12))

                for c_i, col in enumerate(row_cols):
                    holder.grid_columnconfigure(c_i, weight=1)
                    cell = tk.Frame(holder, bg=row_bg, highlightthickness=0, bd=0, cursor="hand2")
                    cell.grid(row=0, column=c_i, padx=(pad_x // 2, pad_x // 2), sticky="n")

                    name = (col.get("name") or "Untitled Collection").strip()
                    # --- blank square placeholder ---
                    tk_img = self._get_collection_tile_photo(col, tile)

                    ph = tk.Canvas(
                        cell,
                        width=tile,
                        height=tile,
                        bg=SHARED_BLANKCOLLECTION_TILEBG_COLOR,
                        highlightthickness=1,
                        highlightbackground=FOCUS_PANEL_ACCENT_COLOR,
                        cursor="hand2",
                    )
                    ph.pack()

                    if tk_img:
                        ph.create_image(tile // 2, tile // 2, image=tk_img)
                        ph._img_ref = tk_img  # prevent GC
                    else:
                        ph.create_rectangle(6, 6, tile - 6, tile - 6, outline=SHARED_BLANKCOLLECTION_TILEACCENT_COLOR)

                    ph.bind("<Button-1>", lambda e, n=name: (self.show_open_collection_page(n), "break"))

                    name_lbl = tk.Label(
        cell,
        text=self._ellipsize_px(name, (SHARED_FONT_TABLE, 16), tile + 40),
        bg=row_bg,
        fg=COLLECTIONS_NAME_FG_COLOR,
                        font=(SHARED_FONT_TABLE, 16),
                        wraplength=tile + 40,
                        justify="center",
                        cursor="hand2",
                    )
                    name_lbl.pack(pady=(8, 0))
                    name_lbl.bind("<Button-1>", lambda e, n=name: (self.show_open_collection_page(n), "break"))


                    count = len(col.get("book_ids") or [])
                    meta = tk.Label(
                        cell,
                        text=f"{count} books",
                        bg=row_bg,
                        fg=COLLECTIONS_META_FG_COLOR,
                        font=(SHARED_FONT_TABLE, 14),
                        cursor="hand2",
                    )
                    meta.pack(pady=(4, 0))
                    meta.bind("<Button-1>", lambda e, n=name: (self.show_open_collection_page(n), "break"))
                    cell.bind("<Button-1>", lambda e, n=name: (self.show_open_collection_page(n), "break"))

            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        def render_list_view(mode: str, reverse: bool = False):
            _force_canvas_window_width()
            clear_scroll_contents()

            rows_sorted = _sort_collections_with_reverse(collections, mode, reverse)

            total_w = max(canvas.winfo_width(), 1)
            total_w = max(total_w - 24, 1)

            # 4 columns: Name, Books, Created, Updated
            name_w = max(int(total_w * 0.45), 280)
            books_w = max(int(total_w * 0.12), 80)
            created_w = max(int(total_w * 0.20), 120)
            updated_w = max(total_w - name_w - books_w - created_w, 120)

            header_font = (SHARED_FONT_TABLE, 18)
            row_font = (SHARED_FONT_TABLE, 18)

            header = tk.Frame(scroll_frame, bg=SHARED_SUBHEADER_BG_COLOR, highlightthickness=0, bd=0)
            header.grid(row=0, column=0, sticky="we")

            col_widths = (name_w, books_w, created_w, updated_w)
            col_weights = (4, 1, 2, 2)

            for i, w in enumerate(col_widths):
                header.grid_columnconfigure(i, minsize=w, weight=col_weights[i])

            # Define clickable header columns
            header_cols = [
                ("Name", 0, "Name"),
                ("Books", 1, "Books"),
                ("Created", 2, "Created"),
                ("Updated", 3, "Last Updated"),
            ]

            current_sort = sort_var.get()
            current_reverse = sort_reverse_var.get()

            for text, col_idx, sort_field in header_cols:
                # Show indicator if this is the current sort
                display_text = text
                if current_sort == sort_field:
                    arrow = "▲" if current_reverse else "▼"
                    display_text = f"{arrow} {text}"

                hdr_lbl = tk.Label(header, text=display_text, bg=SHARED_SUBHEADER_BG_COLOR, fg=SHARED_SUBHEADER_TEXT_COLOR,
                                   font=header_font, anchor="w", padx=12, pady=10, cursor="hand2")
                hdr_lbl.grid(row=0, column=col_idx, sticky="we")

                def _on_header_click(e=None, field=sort_field):
                    current = sort_var.get()
                    if current == field:
                        # Toggle reverse direction
                        sort_reverse_var.set(not sort_reverse_var.get())
                    else:
                        # New column - start with default direction (not reversed)
                        sort_var.set(field)
                        sort_reverse_var.set(False)
                    render_content()

                hdr_lbl.bind("<Button-1>", _on_header_click)

            for idx, col in enumerate(rows_sorted, start=1):
                row_bg = SHARED_TABLE_ALTROW_BG_COLOR if idx % 2 == 0 else SHARED_TABLE_BG_COLOR

                row = tk.Frame(scroll_frame, bg=row_bg, highlightthickness=0, bd=0)
                row.grid(row=idx, column=0, sticky="ew")

                col_widths = (name_w, books_w, created_w, updated_w)
                col_weights = (4, 1, 2, 2)  # name grows most, others grow less

                for i, w in enumerate(col_widths):
                    row.grid_columnconfigure(i, minsize=w, weight=col_weights[i])

                name = (col.get("name") or "Untitled Collection").strip()
                count = len(col.get("book_ids") or [])
                created = self._ts_to_short_date(col.get("created_at") or 0.0)
                updated = self._ts_to_short_date(col.get("updated_at") or 0.0)

                name_txt = self._ellipsize_px(name, row_font, name_w - 24)
                books_txt = str(count)
                created_txt = self._ellipsize_px(created, row_font, created_w - 24)
                updated_txt = self._ellipsize_px(updated, row_font, updated_w - 24)

                cells = [
                    tk.Label(row, text=name_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                             anchor="w", padx=12, pady=8, cursor="hand2"),
                    tk.Label(row, text=books_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                             anchor="w", padx=12, pady=8, cursor="hand2"),
                    tk.Label(row, text=created_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                             anchor="w", padx=12, pady=8, cursor="hand2"),
                    tk.Label(row, text=updated_txt, bg=row_bg, fg=SHARED_SCROLLROW_TEXT_COLOR, font=row_font,
                             anchor="w", padx=12, pady=8, cursor="hand2"),
                ]
                cells[0].grid(row=0, column=0, sticky="we")
                cells[1].grid(row=0, column=1, sticky="we")
                cells[2].grid(row=0, column=2, sticky="we")
                cells[3].grid(row=0, column=3, sticky="we")

                for lbl in cells:
                    lbl.bind("<Button-1>", lambda e, n=(col.get("name") or "").strip(): (self.show_open_collection_page(n), "break"))
                    self.active_widgets.append(lbl)

            canvas.update_idletasks()
            total_w = max(canvas.winfo_width(), 1)
            total_w = max(total_w - 24, 1)
            canvas.configure(scrollregion=canvas.bbox("all"))

        def render_content():
            mode = sort_var.get()
            view = view_var.get()
            reverse = sort_reverse_var.get()
            if view == "list":
                render_list_view(mode, reverse)
            else:
                render_grid_view(mode, reverse)

        # --- NEW: reflow grid when canvas size changes ---
        _resize_after = {"id": None}

        def _on_canvas_resize(_evt=None):
            # only matters for grid view (list already measures widths each render)
            if view_var.get() != "grid":
                return

            if _resize_after["id"] is not None:
                try:
                    canvas.after_cancel(_resize_after["id"])
                except Exception:
                    pass

            _resize_after["id"] = canvas.after(80, render_content)

        canvas.bind("<Configure>", _on_canvas_resize)

        # rebuild radios
        for child in view_btns.winfo_children():
            child.destroy()

        grid_rb = self._make_bubble_radio(
            view_btns, text="Grid", variable=view_var, value="grid", command=render_content, bg=COLLECTIONS_HEADER_BG_COLOR)
        list_rb = self._make_bubble_radio(
            view_btns, text="List", variable=view_var, value="list", command=render_content, bg=COLLECTIONS_HEADER_BG_COLOR)
        self.active_widgets.extend([grid_rb, list_rb])

        sort_var.trace_add("write", lambda *_: render_content())
        render_content()
    def _make_collections_browser_card(self, *, panel_bg: str, header_h: int, collections: list[dict], cols: int = 5):
        container, canvas, scroll_frame = self._make_scroll_container(
            bg=panel_bg,
            relwidth=0.88,
            relheight=0.60,
            top_inset=header_h,
        )

        header = tk.Frame(container, bg=COLLECTIONS_HEADER_BG_COLOR, height=header_h, highlightthickness=0, bd=0)
        header.place(x=0, y=0, relwidth=1.0, height=header_h)
        header.pack_propagate(False)
        self.active_widgets.append(header)

        # Only view controls (no sort dropdown - sorting is done via clickable headers in list view)
        view_var = tk.StringVar(value="list")
        sort_var = tk.StringVar(value="Last Updated")  # Default sort
        sort_reverse_var = tk.BooleanVar(value=False)

        # Inner padding frame
        inner = tk.Frame(header, bg=COLLECTIONS_HEADER_BG_COLOR, highlightthickness=0, bd=0)
        inner.pack(fill="both", expand=True, padx=18, pady=10)
        self.active_widgets.append(inner)

        lbl_font = (SHARED_FONT_TABLE, 18)

        # LEFT: View controls only
        left = tk.Frame(inner, bg=COLLECTIONS_HEADER_BG_COLOR, highlightthickness=0, bd=0)
        left.pack(side="left", anchor="w")
        self.active_widgets.append(left)

        tk.Label(left, text="View:", bg=COLLECTIONS_HEADER_BG_COLOR, fg=COLLECTIONS_HEADER_SUBTEXT_COLOR, font=lbl_font).pack(side="left", padx=(0, 12))
        view_btns = tk.Frame(left, bg=COLLECTIONS_HEADER_BG_COLOR, highlightthickness=0, bd=0)
        view_btns.pack(side="left")
        self.active_widgets.append(view_btns)

        if not collections:
            tk.Label(
                scroll_frame,
                text="No collections available.",
                font=(SHARED_FONT_CUSTOM, 22),
                bg=panel_bg,
                fg=SHARED_SCROLLROW_TEXT_COLOR,
                pady=30,
            ).pack()
            return

        self._render_collections_grid_or_list(
            canvas=canvas,
            scroll_frame=scroll_frame,
            collections=collections,
            sort_var=sort_var,
            view_var=view_var,
            view_btns=view_btns,
            panel_bg=panel_bg,
            cols=cols,
            sort_reverse_var=sort_reverse_var,
        )

        # --- Re-render when the canvas width changes (so list columns stay dynamic) ---
        def _on_canvas_configure(e=None):
            # debounce so we don't rebuild 100x while dragging window
            if hasattr(self, "_collections_resize_after"):
                try:
                    self.after_cancel(self._collections_resize_after)
                except Exception:
                    pass
            self._collections_resize_after = self.after(60, lambda: self._render_collections_grid_or_list(
                canvas=canvas,
                scroll_frame=scroll_frame,
                collections=collections,
                sort_var=sort_var,
                view_var=view_var,
                view_btns=view_btns,
                panel_bg=panel_bg,
                cols=cols,
                sort_reverse_var=sort_reverse_var,
            ))

        canvas.bind("<Configure>", _on_canvas_configure)

    def _norm(self, s: str) -> str:
        s = (s or "").strip().lower()
        return re.sub(r"\s+", " ", s)
    def _book_key(self, b: dict) -> str:
        """
        Stable key to identify a book across lists.

        IMPORTANT: prefer your internal IDs first (book_id/id),
        then fall back to ISBNs, then title.
        """
        for fld in ("book_id", "id", "isbn13", "isbn_13", "isbn10", "isbn_10", "isbn"):
            v = (b.get(fld) or "")
            if isinstance(v, (int, float)):
                v = str(int(v))
            v = str(v).strip()
            if v:
                return v

        return (b.get("title") or "").strip()
    def _book_label(self, b: dict) -> str:
        title = self._unescape_entities(b.get("title") or "Untitled").strip()
        author = (b.get("author") or b.get("authors") or "").strip()
        return f"{title} — {author}" if author else title
    def _all_books(self) -> list[dict]:
        """
        Return the full library as list[dict] for collection-building search.
        Your app's source of truth is self.catalog (backed by LibraryData).
        """
        try:
            # self.catalog is already a list[dict]
            if isinstance(getattr(self, "catalog", None), list):
                return list(self.catalog)

            # fallback: pull straight from LibraryData
            if hasattr(self, "data") and hasattr(self.data, "catalog"):
                return list(self.data.catalog.values())
        except Exception:
            pass

        return []
    def _next_collection_name(self) -> str:
        """
        Always suggest 'Collection 1' for the first collection, then 'Collection 2', etc.
        """
        try:
            existing_recs = self.data.list_collections()  # list[dict]
            existing_names = {
                (r.get("name") or "").strip().lower()
                for r in existing_recs
                if (r.get("name") or "").strip()
            }
        except Exception:
            existing_names = set()

        base = "Collection"
        n = 1
        while f"{base} {n}".lower() in existing_names:
            n += 1

        return f"{base} {n}"

    def _make_scroll_area(
            self,
            parent: tk.Widget,
            x: int,
            y: int,
            w: int,
            h: int,
            *,
            outer_bg: str,
            canvas_bg: str,
            inner_bg: str,
            scrollbar_w: int = 14
    ) -> tuple[tk.Frame, tk.Canvas, tk.Frame]:
        """
        Themed scroll area inside a parent.
        Returns: (outer_frame, canvas, inner_frame)

        IMPORTANT:
        - Outer frame can resize later (fullscreen / window resize).
        - This function attaches metadata to `outer` so relayout code can resize
          the canvas + scrollbar and keep inner window width synced.
        """
        outer = tk.Frame(parent, bg=outer_bg, highlightthickness=0, bd=0)
        outer.place(x=x, y=y, anchor="nw", width=w, height=h)
        self.active_widgets.append(outer)

        canvas = tk.Canvas(outer, bg=canvas_bg, highlightthickness=0, bd=0)
        canvas.place(x=0, y=0, width=max(w - scrollbar_w, 1), height=max(h, 1))

        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        sb.place(x=max(w - scrollbar_w, 1), y=0, width=scrollbar_w, height=max(h, 1))
        canvas.configure(yscrollcommand=sb.set)

        inner = tk.Frame(canvas, bg=inner_bg, highlightthickness=0, bd=0)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        # --- attach references for later relayout ---
        outer._scroll_canvas = canvas
        outer._scroll_sb = sb
        outer._scroll_win_id = win_id
        outer._scrollbar_w = scrollbar_w

        def _sync_inner_width(_evt=None):
            # Keep the inner frame exactly as wide as the *current* canvas width
            try:
                cw = max(canvas.winfo_width(), 1)
                canvas.itemconfigure(win_id, width=cw)
            except Exception:
                pass

        def _on_inner_config(_evt=None):
            # Update scrollregion AND re-sync width
            try:
                canvas.configure(scrollregion=canvas.bbox("all"))
            except Exception:
                pass
            _sync_inner_width()

        inner.bind("<Configure>", _on_inner_config)
        canvas.bind("<Configure>", _sync_inner_width)

        # Mousewheel scroll when hovered
        def _mw(e):
            delta = 0
            if hasattr(e, "delta") and e.delta:
                delta = int(-1 * (e.delta / 120))
            elif getattr(e, "num", None) == 4:
                delta = -1
            elif getattr(e, "num", None) == 5:
                delta = 1
            if delta:
                canvas.yview_scroll(delta, "units")

        canvas.bind("<Enter>", lambda _e: canvas.bind_all("<MouseWheel>", _mw))
        canvas.bind("<Leave>", lambda _e: canvas.unbind_all("<MouseWheel>"))

        return outer, canvas, inner

    # ---------- PAGE: MAIN ----------
    def _search_suggestion_items(self, query: str, *, limit: int = 6):
        """
        Returns list[(label, book)] where label is ONLY:
          - a title OR
          - an author name OR
          - a publisher

        Priority: title matches first, then author, then publisher.
        """
        q = (query or "").strip().lower()
        if not q:
            return []

        titles, authors, pubs = self._build_search_suggestion_index()

        out = []
        seen = set()

        def _add_from(index: dict):
            nonlocal out
            for k, (label, book) in index.items():
                if q in k and k not in seen:
                    seen.add(k)
                    out.append((label, book))
                    if len(out) >= limit:
                        return True
            return False

        # priority order
        if _add_from(titles):
            return out
        if _add_from(authors):
            return out
        _add_from(pubs)
        return out
    def _resolve_recent_search_to_book(self, term: str):
        """
        Best-effort: map a recent search string back to a representative book.
        (title/author/publisher). Returns book or None.
        """
        s = (term or "").strip()
        if not s:
            return None

        titles, authors, pubs = self._build_search_suggestion_index()
        k = s.lower()
        if k in titles:
            return titles[k][1]
        if k in authors:
            return authors[k][1]
        if k in pubs:
            return pubs[k][1]

        # fallback: substring match (title first, then author, then pub)
        for idx in (titles, authors, pubs):
            for kk, (_label, book) in idx.items():
                if k in kk:
                    return book

        return None
    def _open_author_results(self, author_name: str):
        if not hasattr(self, "_search_index"):
            self._search_index = self._build_search_suggestion_index()

        _titles, _authors, _pubs, author_books, _pub_books = self._search_index
        key = (author_name or "").strip().lower()
        books = author_books.get(key, [])
        self._open_search_results_for_books(books, original_query=f"author: {author_name}")
    def _open_publisher_results(self, publisher: str):
        if not hasattr(self, "_search_index"):
            self._search_index = self._build_search_suggestion_index()

        _titles, _authors, _pubs, _author_books, pub_books = self._search_index
        key = (publisher or "").strip().lower()
        books = pub_books.get(key, [])
        self._open_search_results_for_books(books, original_query=f"publisher: {publisher}")
    def _open_search_results_for_books(self, books: list[dict], *, original_query: str):
        """
        Use the SAME renderer perform_search uses:
            self.show_search_results(results, original_query=...)
        """
        results = list(books or [])
        try:
            self.last_search_results = results[:]
            self.last_search_query = (original_query or "").strip().lower()
        except Exception:
            pass

        self.show_search_results(results, original_query=original_query)
    def _build_search_suggestion_index(self):
        """
        Build indices in ONE pass through self.catalog (which is list(self.data.catalog.values())).

        Returns:
          titles:        title_lower -> (display_title, book)
          authors:       author_lower -> display_author
          pubs:          pub_lower -> display_publisher
          author_books:  author_lower -> [book, ...]
          pub_books:     pub_lower -> [book, ...]
        """
        titles = {}
        authors = {}
        pubs = {}
        author_books = {}
        pub_books = {}

        for b in getattr(self, "catalog", []) or []:
            # --- title ---
            t = (b.get("title") or "").strip()
            if t:
                kt = t.lower()
                titles.setdefault(kt, (t, b))

            # --- author display (MATCHES show_book_detail) ---
            first = (b.get("first_name") or "").strip()
            last = (b.get("last_name") or "").strip()
            creators = (b.get("creators") or "").strip()
            author_disp = (f"{first} {last}".strip() if (first or last) else creators).strip()

            if author_disp:
                ka = author_disp.lower()
                authors.setdefault(ka, author_disp)
                author_books.setdefault(ka, []).append(b)

            # --- publisher (backend provides "publisher") ---
            p = b.get("publisher")
            if isinstance(p, list):
                p = (p[0] if p else "")
            p = (p or "").strip()
            if p:
                kp = p.lower()
                pubs.setdefault(kp, p)
                pub_books.setdefault(kp, []).append(b)

        return titles, authors, pubs, author_books, pub_books
    def _suggest_search_items(self, query: str, *, limit: int = 6) -> list[dict]:
        q = (query or "").strip().lower()
        if not q:
            return []

        if not hasattr(self, "_search_index"):
            self._search_index = self._build_search_suggestion_index()

        titles, authors, pubs, _author_books, _pub_books = self._search_index

        out = []
        seen = set()

        # titles first
        for k, (label, book) in titles.items():
            if q in k and k not in seen:
                seen.add(k)
                out.append({"kind": "title", "label": label, "book": book})
                if len(out) >= limit:
                    return out

        # authors second
        for k, label in authors.items():
            if q in k and k not in seen:
                seen.add(k)
                out.append({"kind": "author", "label": label, "book": None})
                if len(out) >= limit:
                    return out

        # publishers last
        for k, label in pubs.items():
            if q in k and k not in seen:
                seen.add(k)
                out.append({"kind": "publisher", "label": label, "book": None})
                if len(out) >= limit:
                    return out

        return out
    def _recent_search_items(self, *, limit: int = 6) -> list[dict]:
        if not hasattr(self, "_search_index"):
            self._search_index = self._build_search_suggestion_index()

        titles, authors, pubs, _author_books, _pub_books = self._search_index

        out = []
        for term in self._get_recent_searches(limit):
            k = (term or "").strip().lower()
            if not k:
                continue

            if k in titles:
                label, book = titles[k]
                out.append({"kind": "title", "label": label, "book": book})
            elif k in authors:
                out.append({"kind": "author", "label": authors[k], "book": None})
            elif k in pubs:
                out.append({"kind": "publisher", "label": pubs[k], "book": None})

        return out
    def show_main_page(self):
        self._search_index = self._build_search_suggestion_index()
        self.set_page("main")
        self.clear_page()
        self.set_background(BG_IMAGE_PATH)
        library_name = self.data.get_library_name()
        self.make_canvas_text(library_name, 0.77, 0.25, self.title_font)

        self.make_canvas_text("Welcome to your personal catalog.", 0.78, 0.35, self.subtitle_font)

        # --- Entry ---
        search_frame, search_entry = self.make_entry_bar(parent=self.canvas)
        search_frame.place(relx=0.5, rely=0.54, anchor="center", width=600, height=35)
        self.active_widgets.extend([search_frame, search_entry])

        # --- Suggestions panel ---
        sug_panel = tk.Frame(
            self,
            bg=BOOKDETAIL_TAGHOLDER_BG_COLOR,
            highlightthickness=1,
            highlightbackground=THEME_COLOR7,
            bd=0,
        )
        sug_panel.place_forget()
        self.active_widgets.append(sug_panel)

        sug_holder = tk.Frame(sug_panel, bg=BOOKDETAIL_TAGHOLDER_BG_COLOR, bd=0, highlightthickness=0)
        sug_holder.pack(fill="both", expand=True, padx=10, pady=8)

        sug_font = (SHARED_FONT_TABLE, 13) if "TABLE_FONT_FAMILY" in globals() else (SHARED_FONT_CUSTOM, 13)
        label_font = (SHARED_FONT_TABLE, 11) if "TABLE_FONT_FAMILY" in globals() else (SHARED_FONT_CUSTOM, 11)

        def _hide_suggestions():
            try:
                # If we've navigated away / widgets destroyed, do nothing
                if self.current_page != "main":
                    return
                if (not sug_panel.winfo_exists()) or (not sug_holder.winfo_exists()):
                    return

                for child in list(sug_holder.winfo_children()):
                    try:
                        child.destroy()
                    except tk.TclError:
                        pass

                sug_panel.place_forget()

            except tk.TclError:
                # Widget already destroyed
                return

        def _handle_search_suggestion(it: dict):
            self._add_recent_search(it["label"])
            _hide_suggestions()

            if it["kind"] == "title" and it.get("book"):
                self.show_book_detail(it["book"])
            elif it["kind"] == "author":
                self._open_author_results(it["label"])
            elif it["kind"] == "publisher":
                self._open_publisher_results(it["label"])
            else:
                self.perform_search(it["label"])

        def _show_suggestions(items: list[dict], label_text: str):
            for child in sug_holder.winfo_children():
                child.destroy()

            if not items:
                _hide_suggestions()
                return

            panel_x = 640
            panel_y = 500 + (35 // 2) + 6
            sug_panel.place(x=panel_x, y=panel_y, anchor="n", width=600)

            sug_panel.update_idletasks()
            available_width = max(sug_panel.winfo_width() - 20, 200)

            row = tk.Frame(sug_holder, bg=BOOKDETAIL_TAGHOLDER_BG_COLOR, bd=0, highlightthickness=0)
            row.pack(fill="x", anchor="w")

            lbl = tk.Label(
                row,
                text=label_text,
                bg=BOOKDETAIL_TAGHOLDER_BG_COLOR,
                fg=BOOKDETAIL_TAGHOLDER_SUBTEXT_COLOR,
                font=label_font,
            )
            lbl.pack(side="left", padx=(0, 6))
            lbl.update_idletasks()
            row_w = lbl.winfo_reqwidth() + 6

            for item in items:
                label = item["label"]
                label = (label[:32] + "…") if len(label) > 32 else label
                chip = tk.Label(
                    row,
                    text=label,
                    bg=BOOKDETAIL_TAGSUGGEST_BG_COLOR,
                    fg=BOOKDETAIL_TAGSUGGEST_TEXT_COLOR,
                    font=sug_font,
                    padx=10,
                    pady=4,
                    cursor="hand2",
                )
                chip.update_idletasks()
                chip_w = chip.winfo_reqwidth() + 6

                if row_w + chip_w > available_width and row_w > (lbl.winfo_reqwidth() + 10):
                    row = tk.Frame(sug_holder, bg=BOOKDETAIL_TAGHOLDER_BG_COLOR, bd=0, highlightthickness=0)
                    row.pack(fill="x", anchor="w", pady=(4, 0))
                    row_w = 0
                    chip.destroy()
                    chip = tk.Label(
                        row,
                        text=label,
                        bg=BOOKDETAIL_TAGSUGGEST_BG_COLOR,
                        fg=BOOKDETAIL_TAGSUGGEST_TEXT_COLOR,
                        font=sug_font,
                        padx=10,
                        pady=4,
                        cursor="hand2",
                    )

                chip.pack(side="left", padx=3, pady=2)
                row_w += chip_w

                # ✅ single, correct binding (no NameError, no duplicate handlers)
                chip.bind("<Button-1>", lambda e, it=item: _handle_search_suggestion(it))

                def _on_enter(e, w=chip):
                    w.configure(bg=BOOKDETAIL_TAGSUGGEST_HOVER_BG_COLOR, fg=BOOKDETAIL_TAGSUGGEST_HOVER_TEXT_COLOR)

                def _on_leave(e, w=chip):
                    w.configure(bg=BOOKDETAIL_TAGSUGGEST_BG_COLOR, fg=BOOKDETAIL_TAGSUGGEST_TEXT_COLOR)

                chip.bind("<Enter>", _on_enter)
                chip.bind("<Leave>", _on_leave)

        def _refresh_suggestions(_evt=None):
            q = search_entry.get().strip()
            if not q:
                items = self._recent_search_items(limit=6)
                _show_suggestions(items, "Recent:")
            else:
                items = self._suggest_search_items(q, limit=6)
                _show_suggestions(items, "Suggestions:")

        def _schedule_hide_if_outside():
            def _check():
                try:
                    # If we've navigated away / widgets destroyed, stop
                    if self.current_page != "main":
                        return
                    if (not sug_panel.winfo_exists()) or (not sug_holder.winfo_exists()):
                        return

                    w = self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())
                    if not w:
                        _hide_suggestions()
                        return
                    if w == search_entry or str(w).startswith(str(sug_panel)):
                        return
                    _hide_suggestions()

                except tk.TclError:
                    # Focus/widget tree changed while callback was pending
                    return

            self.after(120, _check)

        def _do_search(_evt=None):
            term = search_entry.get()
            self._add_recent_search(term)
            _hide_suggestions()
            self.perform_search(term)
            return "break"

        search_entry.bind("<Return>", _do_search)
        search_entry.bind("<KP_Enter>", _do_search)

        search_entry.bind("<FocusIn>", _refresh_suggestions)
        search_entry.bind("<KeyRelease>", _refresh_suggestions)
        search_entry.bind("<FocusOut>", lambda e: _schedule_hide_if_outside())

        search_btn = self.make_button_box(
            "Search",
            lambda: _do_search(),
            (840, 550),
            size=(200, 35),
            font=tkfont.Font(family=SHARED_FONT_CUSTOM, size=22),
        )
        random_btn = self.make_button_box(
            "Suprise Me!",
            self.open_random_book,
            (620, 550),
            size=(200, 35),
            font=tkfont.Font(family=SHARED_FONT_CUSTOM, size=22),
        )

        search_entry.focus_set()
        self.active_widgets.extend([search_btn, random_btn])

    # ---------- PAGE: SETTINGS  ----------
    def show_settings_page(self):
        """Show the settings page."""
        # --- settings button style (prevents NameError) ---
        px_width = 260
        px_height = 44
        bg = SHARED_SCROLL_BG_COLOR
        fg = SHARED_SEARCHBTN_BG_COLOR
        active_bg = FOCUS_PANEL_ACCENT_COLOR
        active_fg = SHARED_SEARCHBTN_BG_ONCLICK_COLOR
        border = SHARED_BUTTON_BORDER_WIDTH
        font = (SHARED_FONT_CUSTOM, 26)

        def settings_button(button_name, button_command, *, relx, rely):
            frame = tk.Frame(
                self.canvas,
                width=px_width,
                height=px_height,
                bg=bg,
                highlightthickness=0,
                bd=0,
            )
            frame.place(relx=relx, rely=rely, anchor="center")
            frame.pack_propagate(False)

            btn = tk.Button(
                frame,
                text=button_name,
                command=lambda: self._safe_call(button_command),
                font=font,
                bg=bg, fg=fg,
                activebackground=active_bg, activeforeground=active_fg,
                bd=border, highlightthickness=0,
                relief="flat", takefocus=False
            )
            btn.pack(fill="both", expand=True)

            self.active_widgets.extend([frame, btn])
            return btn

        self.set_page("settings")
        self.clear_page()
        self.set_background(ASSETS_DIR / "settings.png")

        self.make_canvas_text(
            "Settings",
            0.25, 0.15,
            self.title_font,
        )
        self.make_canvas_text(
            "Manage Library",
            0.7, 0.28,
            self.subtitle_font,
        )

        settings_button("Sync Library",self.gui_download_missing_covers,relx=.75,rely=.35,)
        settings_button("Import CSV", self.gui_import_csv, relx=.75, rely=.42)
        settings_button("Export CSV", self.gui_export_csv, relx=.75, rely=.49)
        settings_button("Factory Reset", self.gui_factory_reset, relx=.75, rely=.56)

        self.make_canvas_text(
            "Library Name",
            0.2, 0.26,
            self.subtitle_font,
        )

        libname_var = tk.StringVar(value=self.data.get_library_name())

        # Container row that resizes with the window (relx/rely/relwidth)
        lib_row = tk.Frame(self.canvas, bg=SHARED_SCROLL_BG_COLOR, highlightthickness=0, bd=0)
        lib_row.place(relx=0.15, rely=0.3, relwidth=0.35, height=30, anchor="nw")
        lib_row.pack_propagate(False)

        # Entry (left)
        entry_frame, entry = self.make_entry_bar(parent=lib_row, textvariable=libname_var,
                                                 font=(SHARED_FONT_CUSTOM, 20))
        entry_frame.place(relx=0.0, rely=0.0, relwidth=0.8, relheight=1.0)

        # Save button (right of the entry)
        btn_bg = SHARED_SCROLL_BG_COLOR
        btn_fg = SHARED_SEARCHBTN_BG_COLOR
        btn_active_bg = FOCUS_PANEL_ACCENT_COLOR
        btn_active_fg = SHARED_SEARCHBTN_BG_ONCLICK_COLOR

        btn_frame = tk.Frame(lib_row, bg=btn_bg, highlightthickness=0, bd=0)
        btn_frame.place(relx=0.80, rely=0.0, relwidth=0.2, relheight=1.0)
        btn_frame.pack_propagate(False)

        def _save_library_name():
            name = (libname_var.get() or "").strip()
            if not name:
                messagebox.showerror("Library Name", "Please enter a library name.")
                return
            saved = self.data.set_library_name(name, persist=True)
            libname_var.set(saved)
            messagebox.showinfo("Saved", f'Library name set to "{saved}".')

        save_btn = tk.Button(
            btn_frame,
            text="Save",
            command=_save_library_name,
            font=(SHARED_FONT_CUSTOM, 20),
            bg=btn_bg, fg=btn_fg,
            activebackground=btn_active_bg, activeforeground=btn_active_fg,
            bd=SHARED_BUTTON_BORDER_WIDTH, highlightthickness=0,
            relief="flat", takefocus=False
        )
        save_btn.pack(fill="both", expand=True)

        # Enter key saves too (nice UX)
        entry.bind("<Return>", lambda _e: _save_library_name())

        self.active_widgets.extend([lib_row, entry_frame, entry, btn_frame, save_btn])

        settings_button("Home", self.go_home, relx=.17, rely=.87, )

        self.update_idletasks()
        # add button that allows user to change library name

    # ---------- PAGE: COLLECTIONS ----------
    def show_collections_page(self):
        self.set_page("collections")
        self.clear_page()
        self.set_background(COLLECTIONS_BG_IMG)
        self._page_img_refs.clear()

        self.update_idletasks()
        win_w = max(self.winfo_width(), 1)
        scale = max(1.0, min(1.35, win_w / 1280))
        title_size = int(round(60 * scale))
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=title_size, weight="bold")

        self.make_canvas_text("Collections", relx=0.5, rely=0.1, font=title_font,)
        self.mount_left_nav()

        collections = self._collections_all()

        # same card layout as Search Results / View All
        self._make_collections_browser_card(
            panel_bg=THEME_COLOR2,
            header_h=60,
            collections=collections,
            cols=5,
        )
    def _sync_scroll_area(self, canvas: tk.Canvas, inner: tk.Frame):
        """
        Make the canvas window match the canvas width and refresh scrollregion.
        Works with your _make_scroll_area() style where the inner frame is embedded
        in the canvas via a canvas window item.
        """
        if not (canvas and canvas.winfo_exists() and inner and inner.winfo_exists()):
            return

        # 1) Force the embedded window to match current canvas width
        wid = getattr(canvas, "_inner_window_id", None)
        if wid is not None:
            try:
                canvas.itemconfigure(wid, width=max(canvas.winfo_width(), 1))
            except Exception:
                pass

        # 2) Update scrollregion
        try:
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        except Exception:
            pass
    def _get_collection_tile_photo(self, col: dict, size_px: int):
        """Return PhotoImage for grid tile if collection has a stored photo."""
        cid = (col.get("collection_id") or "").strip()
        if not cid:
            return None
        try:
            p = self.data.get_collection_photo_path(cid)
        except Exception:
            p = None
        if not p:
            return None
        return self._buildcol_load_preview_photo(str(p), int(size_px))

    def _buildcol_load_preview_photo(self, abs_path: str, size_px: int):
        """
        Load + center-crop to a square, return ImageTk.PhotoImage.
        Cached by (path, size).
        """
        from PIL import Image, ImageTk

        if not abs_path:
            return None

        cache = getattr(self, "_collection_photo_preview_cache", None)
        if cache is None:
            cache = {}
            self._collection_photo_preview_cache = cache

        key = (abs_path, int(size_px))
        if key in cache:
            return cache[key]

        try:
            im = Image.open(abs_path).convert("RGBA")
        except Exception:
            return None

        # Center-crop square then resize
        w, h = im.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        im = im.crop((left, top, left + side, top + side))
        im = im.resize((int(size_px), int(size_px)), Image.LANCZOS)

        tk_img = ImageTk.PhotoImage(im)
        cache[key] = tk_img
        return tk_img

    def _buildcol_refresh_photo_preview(self):
        """Refresh the build-collection photo preview (square placeholder + optional image)."""
        c = getattr(self, "_buildcol_photo_canvas", None)
        if not c or not c.winfo_exists():
            return

        size_px = int(getattr(self, "_buildcol_photo_size_px", 150))
        remove_requested = bool(getattr(self, "_buildcol_photo_remove_requested", False))

        # Keep canvas at the current square size (pixel-perfect)
        try:
            c.place_configure(width=size_px, height=size_px)
        except Exception:
            pass

        # Decide what to show
        abs_path = ""
        if not remove_requested:
            abs_path = (getattr(self, "_buildcol_photo_src_path", "") or "").strip()

            # If editing and no new pick, show stored photo
            if not abs_path:
                cid = getattr(self, "_edit_collection_id", None)
                if cid:
                    try:
                        p = self.data.get_collection_photo_path(cid)
                        abs_path = str(p) if p else ""
                    except Exception:
                        abs_path = ""

        # Clear + redraw
        c.delete("all")

        # Outer “placeholder frame” (always drawn)
        pad = max(6, int(round(size_px * 0.05)))
        c.create_rectangle(
            pad, pad, size_px - pad, size_px - pad,
            outline=FOCUS_PANEL_ACCENT_COLOR,
            width=2
        )

        if abs_path:
            tk_img = self._buildcol_load_preview_photo(abs_path, size_px)
            if tk_img:
                c.create_image(size_px // 2, size_px // 2, image=tk_img)
                c._img_ref = tk_img  # prevent GC
                return

        # No image → draw "No Photo" centered inside the same square
        c._img_ref = None
        c.create_text(
            size_px // 2,
            size_px // 2,
            text="No Photo",
            font=(SHARED_FONT_TABLE, 14),
            fill=COLLECTIONS_NAME_FG_COLOR
        )
    def _buildcol_pick_collection_photo(self):
        """Open file dialog, store chosen path for Save, and refresh preview."""
        from tkinter import filedialog

        path = filedialog.askopenfilename(
            title="Choose a collection photo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.gif"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("WebP", "*.webp"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        self._buildcol_photo_src_path = path
        self._buildcol_photo_remove_requested = False
        self._buildcol_refresh_photo_preview()
    def show_build_collection_page(self, prefill_name: str | None = None, prefill_ids: list[str] | None = None, edit_collection_id: str | None = None):
        """
        Build/edit collection page.
        - edit_collection_id: If provided, we're editing an existing collection (rename instead of create)
        """
        # Store the original collection ID for editing mode
        self._edit_collection_id = edit_collection_id
        original_name = prefill_name  # Track original name for comparison

        def save_collection():
            name = (name_var.get() or "").strip()
            if not name:
                messagebox.showerror("Missing name", "Please enter a collection name.")
                return

            book_ids = list(self._build_collection_selected)
            edit_id = getattr(self, "_edit_collection_id", None)

            try:
                # We will do ONE save at the end for consistent persistence.
                target_cid = None

                if edit_id:
                    # --- EDIT EXISTING ---
                    target_cid = edit_id

                    # Update the book list (no save yet)
                    self.data.set_collection_books(edit_id, book_ids, persist=False)

                    # Rename if changed (no save yet)
                    current_rec = self.data.collections.get(edit_id, {})
                    current_name = (current_rec.get("name") or "").strip()
                    if name.lower() != current_name.lower():
                        self.data.rename_collection(edit_id, name, persist=False)

                    # Photo logic:
                    picked = (getattr(self, "_buildcol_photo_src_path", "") or "").strip()
                    remove_requested = bool(getattr(self, "_buildcol_photo_remove_requested", False))

                    if picked:
                        # Attach/replace photo (no save yet)
                        self.data.set_collection_photo(target_cid, picked, persist=False)
                    elif remove_requested:
                        # User explicitly removed photo (no save yet)
                        self.data.clear_collection_photo(target_cid, persist=False)

                    # Save once
                    self.data.save()
                    rec = self.data.collections.get(edit_id, {"name": name, "book_ids": book_ids})

                else:
                    # --- CREATE (or upsert by name) ---
                    # Use persist=False so we can attach photo first, then save once.
                    rec = self.data.upsert_collection(name, book_ids, persist=False)
                    target_cid = (rec.get("collection_id") or "").strip()

                    picked = (getattr(self, "_buildcol_photo_src_path", "") or "").strip()
                    remove_requested = bool(getattr(self, "_buildcol_photo_remove_requested", False))

                    if picked and target_cid:
                        self.data.set_collection_photo(target_cid, picked, persist=False)
                    elif remove_requested and target_cid:
                        # In create mode this usually won't happen, but safe anyway
                        self.data.clear_collection_photo(target_cid, persist=False)

                    self.data.save()

            except Exception as e:
                messagebox.showerror("Save failed", str(e))
                return

            # Clear the edit mode flag + temp UI state
            self._edit_collection_id = None
            self._buildcol_photo_src_path = ""
            self._buildcol_photo_remove_requested = False

            messagebox.showinfo(
                "Saved",
                f'Saved "{rec.get("name", name)}" with {len(rec.get("book_ids") or [])} books.'
            )
            self.show_collections_page()

        self.set_page("build_collection")


        # --- background ---
        self.clear_page()
        self.set_background(ASSETS_DIR / "collections.png")
        if hasattr(self, "_page_img_refs"):
            self._page_img_refs.clear()

        # --- title ---
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=80, weight="bold")
        self.make_canvas_text("            Build \n Collection", 0.25, 0.3,title_font)

        # --- nav (keeps your home/back/hamburger behavior) ---
        self.mount_left_nav()

        # =========================
        # THEME CONSTANTS (easy later)
        # =========================


        # sizing/placement to match mockup (tweak freely)
        LEFT_X, LEFT_Y, LEFT_W, LEFT_H = 100, 400, 610, 330
        RIGHT_X, RIGHT_Y, RIGHT_W, RIGHT_H = 740, 230, 410, 520

        SELECTED_X, SELECTED_Y, SELECTED_W, SELECTED_H = 30, 140, 350, 300

        # --- panels ---
        left_panel = tk.Frame(self.canvas, bg=BUILDCOLL_LEFTPAN_BG_COLOR, highlightthickness=0, bd=0)
        left_panel.place(x=LEFT_X, y=LEFT_Y, anchor="nw", width=LEFT_W, height=LEFT_H)
        self.active_widgets.append(left_panel)

        right_panel = tk.Frame(self.canvas, bg=BUILDCOLL_RIGHTPAN_BG_COLOR, highlightthickness=0, bd=0)
        right_panel.place(x=RIGHT_X, y=RIGHT_Y, anchor="nw", width=RIGHT_W, height=RIGHT_H)
        self.active_widgets.append(right_panel)

        self._buildcol_left_panel = left_panel
        self._buildcol_right_panel = right_panel

        # ✅ store the *base* layout (your current numbers)
        self._buildcol_layout = {
            "LEFT_X": LEFT_X, "LEFT_Y": LEFT_Y, "LEFT_W": LEFT_W, "LEFT_H": LEFT_H,
            "RIGHT_X": RIGHT_X, "RIGHT_Y": RIGHT_Y, "RIGHT_W": RIGHT_W, "RIGHT_H": RIGHT_H,
            "GAP": 70,  # tweak spacing between cards
        }

        # --- state ---
        self._build_collection_selected = list(prefill_ids or [])

        # --- vars ---
        name_var = tk.StringVar(value=(prefill_name or self._next_collection_name()))
        search_var = tk.StringVar(value="")

        label_font = tkfont.Font(family=SHARED_FONT_TABLE, size=14, weight="bold")
        row_font = tkfont.Font(family=SHARED_FONT_TABLE, size=14)
        plus_font = tkfont.Font(family=SHARED_FONT_TABLE, size=20, weight="bold")

        # =========================
        # RIGHT PANEL: collection name + selected list + save
        # =========================
        name_lbl = tk.Label(
            right_panel,
            text="Collection Name",
            font=label_font,
            bg=BUILDCOLL_RIGHTPAN_BG_COLOR,
            fg=BUILDCOLL_RIGHTPAN_HEADER_TEXT_COLOR,
            anchor="e",
        )
        # Place once for initial render; relayout will keep it aligned on resize
        name_lbl.place(x=30 + (RIGHT_W - 60), y=16, anchor="ne")
        self.active_widgets.append(name_lbl)
        self._buildcol_name_lbl = name_lbl

        name_frame, name_entry = self.make_entry_bar(
            parent=right_panel,
            textvariable=name_var,
            font=(ENTRY_BAR_FONT_FAMILY, SHARED_ENTRY_FONT_SIZE),
        )
        name_frame.place(x=30, y=45, anchor="nw", width=RIGHT_W - 60, height=36)
        self.active_widgets.extend([name_frame, name_entry])
        self._buildcol_name_frame = name_frame

        selected_title = tk.Label(
            right_panel,
            text="In this collection",
            font=label_font,
            bg=BUILDCOLL_RIGHTPAN_BG_COLOR,
            fg=BUILDCOLL_RIGHTPAN_SUB_TEXT_COLOR,
        )
        selected_title.place(x=SELECTED_X + (SELECTED_W // 2), y=92, anchor="n")
        self.active_widgets.append(selected_title)
        self._buildcol_selected_title = selected_title

        selected_outer, selected_canvas, selected_inner = self._make_scroll_area(
            parent=right_panel,
            x=SELECTED_X,
            y=SELECTED_Y,
            w=SELECTED_W,
            h=SELECTED_H,
            outer_bg=BUILDCOLL_RIGHTPAN_BG_COLOR,
            canvas_bg=BUILDCOLL_RIGHTPAN_LIST_BG_COLOR,
            inner_bg=BUILDCOLL_RIGHTPAN_LIST_BG_COLOR,
        )
        self._buildcol_selected_outer = selected_outer
        self._buildcol_selected_canvas = selected_canvas
        self._buildcol_selected_inner = selected_inner

        # Save button INSIDE the right panel, directly under the selected list
        save_y = SELECTED_Y + SELECTED_H + 12  # right below the list
        save_btn = tk.Button(
            right_panel,
            text="Save Collection",
            command=save_collection,
            font=tkfont.Font(family=SHARED_FONT_CUSTOM, size=22),
            bg=SHARED_BUTTON1_BG_COLOR,
            fg=SHARED_BUTTON1_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            bd=SHARED_BUTTON_BORDER_WIDTH,
            relief="flat",
            cursor="hand2",
        )
        save_btn.place(x=SELECTED_X, y=save_y, anchor="nw", width=SELECTED_W, height=45)
        self.active_widgets.append(save_btn)
        self._buildcol_save_btn = save_btn

        # =========================
        # LEFT PANEL: search label + entry + results list with + gutter
        # =========================
        search_lbl = tk.Label(
            left_panel,
            text="Search books to add",
            font=label_font,
            bg=BUILDCOLL_LEFTPAN_BG_COLOR,
            fg=BUILDCOLL_LEFTPAN_HEADER_TEXT_COLOR,
            anchor="w",
        )
        search_lbl.place(x=20, y=16, anchor="nw")
        self.active_widgets.append(search_lbl)

        search_frame, search_entry = self.make_entry_bar(
            parent=left_panel,
            textvariable=search_var,
            font=(ENTRY_BAR_FONT_FAMILY, SHARED_ENTRY_FONT_SIZE),
        )
        search_frame.place(x=20, y=45, anchor="nw", width=LEFT_W - 40, height=36)
        self.active_widgets.extend([search_frame, search_entry])
        self._buildcol_search_frame = search_frame

        results_outer, results_canvas, results_inner = self._make_scroll_area(
            parent=left_panel,
            x=20,
            y=90,
            w=LEFT_W - 40,
            h=LEFT_H - 110,
            outer_bg=BUILDCOLL_LEFTPAN_LIST_TEXT_COLOR,
            canvas_bg=BUILDCOLL_LEFTPAN_LIST_BG_COLOR,
            inner_bg=BUILDCOLL_LEFTPAN_LIST_BG_COLOR,
        )
        self._buildcol_results_outer = results_outer
        self._buildcol_results_canvas = results_canvas
        self._buildcol_results_inner = results_inner

        # Ensure entry bars are visible immediately on first render
        name_frame.lift()
        search_frame.lift()
        self.canvas.update_idletasks()

        # =========================
        # helpers
        # =========================
        def clear_inner(frame: tk.Frame):
            for w in frame.winfo_children():
                w.destroy()

        def current_matches() -> list[dict]:
            q = self._norm(search_var.get())
            books = self._all_books()

            if not q:
                return books[:50]

            out = []
            for b in books:
                hay = " ".join([
                    self._norm(b.get("title", "")),
                    self._norm(b.get("author", "")),
                    self._norm(b.get("subjects", "")),
                    self._norm(b.get("genre", "")),
                ])
                if q in hay:
                    out.append(b)
            return out[:100]

        def add_book(book_key: str):
            if not book_key:
                return
            if book_key not in self._build_collection_selected:
                self._build_collection_selected.append(book_key)
            render_selected()
            render_results()

        def remove_book(book_key: str):
            if book_key in self._build_collection_selected:
                self._build_collection_selected.remove(book_key)
            render_selected()
            render_results()

        def render_results():
            clear_inner(results_inner)
            books = current_matches()

            for b in books:
                k = self._book_key(b)
                if not k:
                    continue

                row = tk.Frame(results_inner, bg=BUILDCOLL_LEFTPAN_LIST_BG_COLOR,highlightthickness=0, bd=0)
                row.pack(fill="x", padx=0, pady=0)

                # "+" gutter cell (gray strip look)
                gutter = tk.Frame(row, bg=BUILDCOLL_LEFTPAN_LIST_BG_COLOR, width=44, height=40, highlightthickness=0, bd=0)
                gutter.pack(side="left", fill="y")
                gutter.pack_propagate(False)

                already = (k in self._build_collection_selected)
                plus_btn = tk.Button(
                    gutter,
                    text="+",
                    font=plus_font,
                    command=(lambda kk=k: add_book(kk)),
                    state=("disabled" if already else "normal"),
                    bg=BUILDCOLL_PLUSBTN_BG_COLOR,
                    fg=BUILDCOLL_PLUSBTN_CLICKABLE_COLOR,
                    activebackground=BUILDCOLL_PLUSICON_ONCLICK_COLOR,
                    activeforeground=BUILDCOLL_PLUSICON_ONCLICK_COLOR,
                    bd=1,
                    relief="solid",
                    cursor="hand2",
                )
                plus_btn.place(relx=0.5, rely=0.5, anchor="center", width=34, height=34)
                self.active_widgets.append(plus_btn)

                # text cell with wrapping so long titles wrap to new line
                txt = tk.Label(
                    row,
                    text=self._book_label(b),
                    font=row_font,
                    bg=BUILDCOLL_LEFTPAN_LIST_BG_COLOR,
                    fg=BUILDCOLL_LEFTPAN_LIST_TEXT_COLOR,
                    anchor="w",
                    justify="left",
                    wraplength=480,  # Wrap text to prevent overflow (left panel is wider)
                    padx=10,
                    pady=8,
                )
                txt.pack(side="left", fill="x", expand=True)
                self.active_widgets.append(txt)

                # separator
                tk.Frame(results_inner, bg=BUILDCOLL_LEFTPAN_BG_COLOR, height=1).pack(fill="x")

        def _do_search(event=None):
            render_results()
            return "break"  # stop Tk from doing any default beep/propagation


        search_entry.bind("<KP_Enter>", _do_search)  # keypad Enter too (optional)
        search_entry.focus_set()  # optional: cursor starts in the search box

        # --- collection photo (preview + controls) ---
        self._buildcol_photo_src_path = ""
        self._buildcol_photo_remove_requested = False
        self._buildcol_photo_size_px = 150  # relayout will adjust

        photo_holder = tk.Frame(self.canvas, bg=BUILDCOLL_LEFTPAN_BG_COLOR, highlightthickness=0, bd=0)
        # NOTE: relayout will place/size this; these are just safe defaults
        photo_holder.place(x=460, y=230, anchor="nw", width=220, height=260)
        self.active_widgets.append(photo_holder)

        # Square preview area (Canvas so "No Photo" can be centered with a border)
        preview_border = FOCUS_PANEL_ACCENT_COLOR
        photo_canvas = tk.Canvas(
            photo_holder,
            bg=BUILDCOLL_LEFTPAN_BG_COLOR,
            highlightthickness=1,
            highlightbackground=preview_border,
            bd=0,
        )
        # IMPORTANT: use place for EVERYTHING inside photo_holder (no pack/grid)
        photo_canvas.place(x=16, y=12, width=self._buildcol_photo_size_px, height=self._buildcol_photo_size_px)
        photo_canvas.bind("<Button-1>", lambda e: (self._buildcol_pick_collection_photo(), "break"))
        self._buildcol_photo_canvas = photo_canvas

        # Buttons go BELOW the square preview
        btn_row = tk.Frame(photo_holder, bg=BUILDCOLL_LEFTPAN_BG_COLOR, highlightthickness=0, bd=0)
        btn_row.place(x=16, y=12 + self._buildcol_photo_size_px + 10, width=self._buildcol_photo_size_px, height=42)
        self._buildcol_photo_btn_row = btn_row  # <-- save for relayout

        def _remove_photo():
            # UI-state: show placeholder immediately
            self._buildcol_photo_src_path = ""
            self._buildcol_photo_remove_requested = True

            # If editing an existing collection, persist the delete immediately
            cid = getattr(self, "_edit_collection_id", None)
            if cid:
                try:
                    self.data.clear_collection_photo(cid, persist=True)
                except Exception:
                    pass

            self._buildcol_refresh_photo_preview()

        upload_btn = tk.Button(
            btn_row,
            text="Upload",
            command=self._buildcol_pick_collection_photo,
            bg=SHARED_BUTTON1_BG_COLOR,
            fg=SHARED_BUTTON1_TEXT_COLOR,
            bd=0,
            highlightthickness=1,
            highlightbackground=FOCUS_PANEL_ACCENT_COLOR,
            font=(SHARED_FONT_BUTTON, 12),
            padx=12,
            pady=6,
        )
        upload_btn.place(x=0, y=0, width=(self._buildcol_photo_size_px // 2) - 6, height=42)

        remove_btn = tk.Button(
            btn_row,
            text="Remove",
            command=_remove_photo,
            bg=SHARED_BUTTON1_BG_COLOR,
            fg=SHARED_BUTTON1_TEXT_COLOR,
            bd=0,
            highlightthickness=1,
            highlightbackground=FOCUS_PANEL_ACCENT_COLOR,
            font=(SHARED_FONT_BUTTON, 12),
            padx=12,
            pady=6,
        )
        remove_btn.place(x=(self._buildcol_photo_size_px // 2) + 6, y=0, width=(self._buildcol_photo_size_px // 2) - 6,
                         height=42)

        self._buildcol_photo_holder = photo_holder

        # initial preview (important for edit mode)
        self._buildcol_refresh_photo_preview()



        def render_selected():
            clear_inner(selected_inner)
            all_books = {self._book_key(b): b for b in self._all_books()}

            for k in self._build_collection_selected:
                b = all_books.get(k, {"title": k})

                row = tk.Frame(selected_inner, bg=BUILDCOLL_RIGHTPAN_BG_COLOR, highlightthickness=0, bd=0)
                row.pack(fill="x")

                # Gutter for x button (same structure as + button on left panel)
                gutter = tk.Frame(row, bg=BUILDCOLL_RIGHTPAN_LIST_BG_COLOR, width=50, highlightthickness=0, bd=0)
                gutter.pack(side="right", fill="y")
                gutter.pack_propagate(False)

                rm_btn = tk.Button(
                    gutter,
                    text="×",
                    font=plus_font,  # Use same font as + button
                    command=(lambda kk=k: remove_book(kk)),
                    bg=SHARED_XBTN_BG_COLOR,
                    fg=SHARED_XBTN_IDLE_COLOR,
                    activebackground=SHARED_XBTN_BG_ONCLICK_COLOR,
                    activeforeground=SHARED_XBTN_SELECTED_ONCLICK_COLOR,
                    bd=1,
                    relief="solid",
                    cursor="hand2",
                )
                rm_btn.place(relx=0.5, rely=0.5, anchor="center", width=34, height=34)
                self.active_widgets.append(rm_btn)

                # Text label with wrapping so long titles wrap to new line
                txt = tk.Label(
                    row,
                    text=self._book_label(b),
                    font=row_font,
                    bg=BUILDCOLL_RIGHTPAN_LIST_BG_COLOR,
                    fg=BUILDCOLL_RIGHTPAN_LIST_TEXT_COLOR,
                    anchor="w",
                    justify="left",
                    wraplength=240,  # Reduced to give more space before x button
                    padx=10,
                    pady=8,
                )
                txt.pack(side="left", fill="x", expand=True)
                self.active_widgets.append(txt)

                tk.Frame(selected_inner, bg=BUILDCOLL_RIGHTPAN_BG_COLOR, height=1).pack(fill="x")

        # live search
        search_entry.bind("<Return>", lambda e: (render_results(), "break"))
        search_entry.bind("<KP_Enter>", lambda e: (render_results(), "break"))

        render_results()
        render_selected()
        self.after_idle(self._buildcol_relayout)
        self.after(50, self._buildcol_relayout)
    def _buildcol_relayout(self):
        def _resize_scroll_outer(outer_frame: tk.Frame, new_w: int, new_h: int):
            if not outer_frame or not outer_frame.winfo_exists():
                return

            canvas = getattr(outer_frame, "_scroll_canvas", None)
            sb = getattr(outer_frame, "_scroll_sb", None)
            win_id = getattr(outer_frame, "_scroll_win_id", None)
            sbw = int(getattr(outer_frame, "_scrollbar_w", 14))

            if not canvas or not sb or win_id is None:
                return

            new_w = max(int(new_w), 1)
            new_h = max(int(new_h), 1)
            canvas_w = max(new_w - sbw, 1)

            # Resize the canvas + scrollbar (they use place, so they do NOT auto-resize)
            canvas.place_configure(x=0, y=0, width=canvas_w, height=new_h)
            sb.place_configure(x=canvas_w, y=0, width=sbw, height=new_h)

            # Keep inner window width matched to the new canvas width
            try:
                canvas.itemconfigure(win_id, width=canvas_w)
                canvas.configure(scrollregion=canvas.bbox("all"))
            except Exception:
                pass

        if getattr(self, "current_page", "") != "build_collection":
            return

        left = getattr(self, "_buildcol_left_panel", None)
        right = getattr(self, "_buildcol_right_panel", None)
        layout = getattr(self, "_buildcol_layout", None)
        if not left or not right or not layout:
            return
        if not (left.winfo_exists() and right.winfo_exists()):
            return

        # ---- base numbers (your original constants) ----
        LEFT_X = int(layout["LEFT_X"])
        LEFT_Y = int(layout["LEFT_Y"])
        LEFT_W = int(layout["LEFT_W"])
        LEFT_H = int(layout["LEFT_H"])
        RIGHT_X = int(layout["RIGHT_X"])
        RIGHT_Y = int(layout["RIGHT_Y"])
        RIGHT_W = int(layout["RIGHT_W"])
        RIGHT_H = int(layout["RIGHT_H"])
        GAP = int(layout.get("GAP", 70))

        # ---- grow cards slightly with window width (but cap it) ----
        win_w = max(self.winfo_width(), 1)
        s = max(1.0, min(1.18, win_w / 1280))

        new_left_w = int(round(LEFT_W * s))
        new_left_h = int(round(LEFT_H * s))
        new_right_w = int(round(RIGHT_W * s))
        new_right_h = int(round(RIGHT_H * s))

        # ---- center the pair as a group ----
        group_w = new_left_w + GAP + new_right_w
        canvas_w = max(self.canvas.winfo_width(), 1)
        start_x = int((canvas_w - group_w) / 2)

        new_left_x = start_x
        new_right_x = start_x + new_left_w + GAP

        new_left_y = LEFT_Y
        new_right_y = RIGHT_Y

        # ---- apply panel geometry ----
        left.place_configure(x=new_left_x, y=new_left_y, width=new_left_w, height=new_left_h)
        right.place_configure(x=new_right_x, y=new_right_y, width=new_right_w, height=new_right_h)

        # ---- update entry widths ----
        search_frame = getattr(self, "_buildcol_search_frame", None)
        if search_frame and search_frame.winfo_exists():
            search_frame.place_configure(width=max(new_left_w - 40, 200))

        name_frame = getattr(self, "_buildcol_name_frame", None)
        if name_frame and name_frame.winfo_exists():
            name_frame.place_configure(width=max(new_right_w - 60, 200))

        # ---- LEFT scroll area ----
        results_outer = getattr(self, "_buildcol_results_outer", None)
        if results_outer and results_outer.winfo_exists():
            new_res_w = max(new_left_w - 40, 200)
            new_res_h = max(new_left_h - 110, 120)
            results_outer.place_configure(width=new_res_w, height=new_res_h)
            _resize_scroll_outer(results_outer, new_res_w, new_res_h)

        # ---- RIGHT selected list sizing ----
        selected_outer = getattr(self, "_buildcol_selected_outer", None)

        # Keep your original x/y (SELECTED_X/Y), but grow width with the panel
        # Your original margins: left/right margin ~30 each => total 60
        pad_lr = 60
        new_sel_w = max(new_right_w - pad_lr, 220)
        new_sel_h = max(int(round(300 * s)), 220)

        if selected_outer and selected_outer.winfo_exists():
            selected_outer.place_configure(width=new_sel_w, height=new_sel_h)
            _resize_scroll_outer(selected_outer, new_sel_w, new_sel_h)

        # -------------------------
        # RIGHT PANEL LABEL ALIGNMENT (always run)
        # -------------------------
        name_lbl = getattr(self, "_buildcol_name_lbl", None)
        if name_lbl and name_lbl.winfo_exists() and name_frame and name_frame.winfo_exists():
            name_frame.update_idletasks()
            ex = int(name_frame.winfo_x())
            ew = int(name_frame.winfo_width())
            # right edge of the entry frame
            name_lbl.place_configure(x=ex + ew, y=16, anchor="ne")

        selected_title = getattr(self, "_buildcol_selected_title", None)
        if selected_title and selected_title.winfo_exists():
            # Center it over the selected list region.
            # We center using the selected_outer if available, otherwise fall back to computed width.
            if selected_outer and selected_outer.winfo_exists():
                selected_outer.update_idletasks()
                sx = int(selected_outer.winfo_x())
                sw = int(selected_outer.winfo_width())
                cx = sx + (sw // 2)
            else:
                # fallback: list is at x=30 in right_panel, width=new_sel_w
                cx = 30 + (new_sel_w // 2)

            selected_title.place_configure(x=cx, y=92, anchor="n")

        # -------------------------
        # Save button: keep below list AND match list width
        # -------------------------
        save_btn = getattr(self, "_buildcol_save_btn", None)
        if save_btn and save_btn.winfo_exists():
            if selected_outer and selected_outer.winfo_exists():
                info = selected_outer.place_info()
                sel_y = int(float(info.get("y", 140)))
                sel_h = int(float(info.get("height", new_sel_h)))
            else:
                sel_y = 140
                sel_h = new_sel_h

            save_btn.place_configure(y=sel_y + sel_h + 12, width=new_sel_w)

        # -------------------------
        # Collection photo: dock it LEFT of the right panel (above left panel)
        # -------------------------
        photo_holder = getattr(self, "_buildcol_photo_holder", None)
        if photo_holder and photo_holder.winfo_exists():
            size_px = int(round(250 * s))
            size_px = max(110, min(size_px, 175))
            self._buildcol_photo_size_px = size_px

            margin = int(round(14 * s))
            holder_w = size_px + 2 * margin
            holder_h = size_px + int(round(58 * s)) + margin  # preview + buttons + padding

            # X: position so the holder's RIGHT edge hugs the LEFT edge of the right panel
            pad_to_right_panel = int(round(65 * s))
            x = new_right_x - holder_w - pad_to_right_panel

            # Clamp so it doesn't spill past the left panel's right edge too much
            # (we actually want it in that lane between panels)
            left_lane_min = new_left_x + new_left_w - holder_w + int(round(10 * s))
            left_lane_max = new_right_x - holder_w - int(round(6 * s))
            x = max(left_lane_min, min(x, left_lane_max))

            # Y: sit in the vertical lane between top of right panel and top of left panel
            top_slot = new_right_y + margin
            bottom_slot = new_left_y - holder_h - margin

            if bottom_slot < top_slot:
                # Not enough space; fall back to “near top of right panel”
                y = new_right_y + int(round(-100 * s))
            else:
                y = top_slot + (bottom_slot - top_slot) // 2
                y = y - int(round(35 * s))  # bias upward
                y = max(top_slot, min(y, bottom_slot))

            photo_holder.place_configure(x=int(x), y=int(y), width=int(holder_w), height=int(holder_h))

            # Preview square
            c = getattr(self, "_buildcol_photo_canvas", None)
            if c and c.winfo_exists():
                c.place_configure(x=margin, y=margin, width=size_px, height=size_px)

            # Button row
            btn_row = getattr(self, "_buildcol_photo_btn_row", None)
            if btn_row and btn_row.winfo_exists():
                btn_row.place_configure(
                    x=margin,
                    y=margin + size_px + int(round(10 * s)),
                    width=size_px,
                    height=int(round(42 * s)),
                )

            self._buildcol_refresh_photo_preview()

    # ---------- PAGE: BROWSE GENRES ----------
    def _available_genres_for_tab(self, tab: str) -> list[str]:
        """
        Returns genres that currently exist in the library for the selected tab.
        - fiction: Only fiction starter genres with books
        - nonfiction: Only nonfiction starter genres with books
        - all: ALL genres present in the library (starter + custom + any legacy) with books
        - custom: Only custom (non-starter) genres with books
        """
        found = {(b.get("genre") or "").strip().title() for b in (self.catalog or [])}
        found.discard("")  # remove empty

        starter = {
            g.strip().title()
            for g in (
                    getattr(self.data, "FICTION_GENRES", [])
                    + getattr(self.data, "NONFICTION_GENRES", [])
            )
        }

        if tab == "fiction":
            allowed = [g.strip().title() for g in getattr(self.data, "FICTION_GENRES", [])]
            return [g for g in allowed if g in found]

        if tab == "nonfiction":
            allowed = [g.strip().title() for g in getattr(self.data, "NONFICTION_GENRES", [])]
            return [g for g in allowed if g in found]

        if tab == "all":
            # ✅ truly "all": includes custom genres
            return sorted(found, key=str.lower)

        if tab == "custom":
            # Custom = genres used by books that are NOT starter genres
            try:
                user_genres = {g.strip().title() for g in self.data.get_user_genres()}
            except Exception:
                user_genres = set()

            custom_in_books = {g for g in found if g not in starter}
            custom_in_books |= {g for g in user_genres if g in found}
            return sorted(custom_in_books, key=str.lower)

        allowed = [g.strip().title() for g in getattr(self.data, "FICTION_GENRES", [])]
        return [g for g in allowed if g in found]

    def show_browse_genres_page(self, selected_tab="all"):
        self.set_page("browse_genres", tab=selected_tab)

        self.clear_page()
        self.set_background(BROWSE_GENRES_BG_IMG)
        self.update_idletasks()

        w = self.winfo_width()
        fs_like = self._is_fullscreen_like()

        genres = self._available_genres_for_tab(selected_tab)

        # Title font scaling
        try:
            browse_font = tkfont.Font(font=self.title_font)
            base = browse_font.cget("size")
            browse_font.configure(size=int(base * (1.15 if fs_like else 1.0)))
        except Exception:
            browse_font = self.title_font

        self.make_canvas_text("Browse Genres", 0.5, 0.2, browse_font)

        try:
            self.genre_font.configure(size=22 if fs_like else 20)
            self.left_button_font.configure(size=22 if fs_like else 20)
        except Exception:
            pass

        self.mount_left_nav()

        category_frame = tk.Frame(self.canvas, bg=SHARED_MINILABEL_BG_COLOR, highlightthickness=0, bd=0)
        category_frame.place(relx=.83, rely=.24, anchor="center", width=220, height=50)
        self.active_widgets.append(category_frame)

        category_label = tk.Label(
            category_frame,
            text="Category:",
            bg=SHARED_MINILABEL_BG_COLOR,
            fg=SHARED_MINILABEL_TEXT_COLOR,
            font=(SHARED_FONT_CUSTOM, 22),
        )
        category_label.pack(side="left", padx=(10, 10), pady=10)
        self.active_widgets.append(category_label)

        # Map display names to internal tab values
        category_options = ["All","Fiction", "Non-Fiction", "Custom"]
        tab_to_display = {
            "all": "All",
            "fiction": "Fiction",
            "nonfiction": "Non-Fiction",
            "custom": "Custom"
        }
        display_to_tab = {v: k for k, v in tab_to_display.items()}

        category_var = tk.StringVar(value=tab_to_display.get(selected_tab, "All"))

        category_combo = ttk.Combobox(
            category_frame,
            textvariable=category_var,
            values=category_options,
            state="readonly",
            font=(SHARED_FONT_CUSTOM, 20),
            width=10,
        )
        category_combo.pack(side="left", padx=(0, 10), pady=10)
        self.active_widgets.append(category_combo)

        def _on_category_change(event=None):
            new_tab = display_to_tab.get(category_var.get(), "all")
            if new_tab != selected_tab:
                self.show_browse_genres_page(new_tab)

        category_combo.bind("<<ComboboxSelected>>", _on_category_change)

        panel = tk.Frame(self.canvas, bg=BROWSEGENRES_GRID_BG_COLOR, highlightthickness=0, bd=0)
        panel.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.86, relheight=0.50)

        # Use matching background to prevent flash - canvas starts hidden until first render
        grid_canvas = tk.Canvas(panel, bg=BROWSEGENRES_GRID_BG_COLOR, highlightthickness=0, bd=0)
        vbar = tk.Scrollbar(panel, orient="vertical", command=grid_canvas.yview)
        grid_canvas.configure(yscrollcommand=vbar.set)

        vbar.pack(side="right", fill="y")
        grid_canvas.pack(side="left", fill="both", expand=True)

        grid_frame = tk.Frame(grid_canvas, bg=BROWSEGENRES_GRID_BG_COLOR, highlightthickness=0, bd=0)
        window_id = grid_canvas.create_window((0, 0), window=grid_frame, anchor="nw")

        self._register_scroll_canvas(grid_canvas)
        self.active_widgets.extend([panel, grid_canvas, vbar, grid_frame])

        btn_h = 70 if fs_like else 60
        gap_x = 18
        gap_y = 18
        btn_min_w = 220 if fs_like else 200
        MAX_COLS = 6 if fs_like else 4

        def render_genres_now():
            self._render_genre_buttons(
                grid_frame=grid_frame,
                grid_canvas=grid_canvas,
                genres=genres,
                fs_like=fs_like,
                gap_x=gap_x,
                gap_y=gap_y,
                btn_min_w=btn_min_w,
                btn_h=btn_h,
                max_cols=MAX_COLS,
            )
            try:
                grid_canvas.configure(scrollregion=grid_canvas.bbox("all"))
            except Exception:
                pass

        # --- debounced width-sync + render (prevents jitter feedback loop) ---
        _grid_render_after = {"id": None}
        _last_w = {"w": 0}

        def _schedule_render():
            # cancel any pending render
            if _grid_render_after["id"] is not None:
                try:
                    grid_canvas.after_cancel(_grid_render_after["id"])
                except Exception:
                    pass
                _grid_render_after["id"] = None

            # schedule a single render shortly after geometry settles
            _grid_render_after["id"] = grid_canvas.after(40, render_genres_now)

        def on_canvas_configure(event):
            # Only react if width changed enough to matter (prevents tiny oscillations)
            w = int(event.width)
            if abs(w - _last_w["w"]) < 6:
                return
            _last_w["w"] = w

            try:
                grid_canvas.itemconfig(window_id, width=w)
            except Exception:
                return

            _schedule_render()

        grid_canvas.bind("<Configure>", on_canvas_configure)

        def _first_render_when_ready():
            if getattr(self, "current_page", None) != "browse_genres":
                return
            if grid_canvas.winfo_width() <= 2:
                grid_canvas.after(16, _first_render_when_ready)
                return
            render_genres_now()

        grid_canvas.after_idle(_first_render_when_ready)
    def show_genre_page(self, genre_name: str):
        """Show all books in a specific genre."""
        self._show_filtered_books_page(
            page_type="genre",
            filter_value=genre_name,
        )
    def _show_filtered_books_page(self,page_type: str,filter_value: str,letter_filter: str | None = None,filter_field: str = "Title",):
        """
        Unified page for showing filtered book lists (genre, tag).
        Includes alphabet filter bar and view/sort controls.
        
        Args:
            page_type: "genre" or "tag"
            filter_value: The genre name or tag name
            letter_filter: Optional letter to filter by
            filter_field: Field to filter by ("Title", "Author (Last Name)", "Year")
        """
        filter_value = (filter_value or "").strip()
        if not filter_value:
            self.perform_search("")
            return

        page_name = f"{page_type}_page"
        self.set_page(page_name, **{page_type: filter_value, "letter_filter": letter_filter, "filter_field": filter_field})

        self.clear_page()
        if page_type == "genre":
            self.set_background(ASSETS_DIR / "selected genre.png")
        else:
            self.set_background(SHOW_BOOKS_BG_IMG)
        self._page_img_refs.clear()
        self.mount_left_nav()

        self.update_idletasks()
        win_w = max(self.winfo_width(), 1)

        scale = max(1.0, min(1.35, win_w / 1280))
        title_size = int(round(60 * scale))
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=title_size, weight="bold")

        # Title
        if page_type == "genre":
            title_text = filter_value
            context_label = f"Genre: {filter_value}"
        else:
            title_text = f"Tag: {filter_value}"
            context_label = f"Tag: {filter_value}"

        self.make_canvas_text(title_text, relx=0.5, rely=0.9, font=title_font)

        # Get books
        if page_type == "genre":
            all_filtered_books = self._filter_books_by_genre(filter_value)
        else:
            all_filtered_books = self._filter_books_by_tag(filter_value)

        # Apply letter filter if set
        if letter_filter:
            books = [b for b in all_filtered_books if self._get_filter_first_char(b, filter_field) == letter_filter]
            field_display = filter_field
            if filter_field == "Author (Last Name)":
                field_display = "Author"
            if letter_filter == "#":
                context_label = f"{context_label} ({field_display}: 0-9)"
            elif letter_filter == "~":
                context_label = f"{context_label} ({field_display}: Symbols)"
            else:
                context_label = f"{context_label} ({field_display}: {letter_filter})"
        else:
            books = all_filtered_books

        # Alphabet filter bar callback
        def on_filter_change(new_letter: str | None, new_field: str):
            self._show_filtered_books_page(
                page_type=page_type,
                filter_value=filter_value,
                letter_filter=new_letter,
                filter_field=new_field,
            )

        # Create alphabet bar - starts at rely=0.17
        alphabet_bar_rely = 0.1
        self._make_alphabet_filter_bar(
            books=all_filtered_books,
            filter_field=filter_field,
            letter_filter=letter_filter,
            on_filter_change=on_filter_change,
            show_filter_dropdown=True,
            rely=alphabet_bar_rely,
        )

        # Scroll container - use pixel offset from alphabet bar
        # Alphabet bar is 36px tall, so container top = alphabet_bar top + 36px
        container, canvas, scroll_frame = self._make_scroll_container(
            bg=SHARED_TABLE_BG_COLOR,
            relwidth=0.88,
            relheight=0.70,
            top_inset=60,
        )

        # Position container so its top aligns exactly with bottom of alphabet bar
        # Using y offset of 36 (alphabet bar height) from the alphabet bar's rely position
        container.place_configure(relx=0.5, rely=alphabet_bar_rely, y=36, anchor="n")

        header = tk.Frame(container, bg=SHARED_MAINHEADER_BG_COLOR, height=60, highlightthickness=0, bd=0)
        header.place(x=0, y=0, relwidth=1.0, height=60)
        header.pack_propagate(False)
        self.active_widgets.append(header)

        sort_var, view_var, view_btns, secondary_sort_var, secondary_sort_reverse_var = self._make_sort_and_view_controls(
            header,
            bg=SHARED_MAINHEADER_BG_COLOR,
            pad_x=18,
            pad_y=10,
            default_view="list",
            default_sort="Title",
            sort_values=("Title", "Author", "Year")
        )

        if not books:
            tk.Label(
                scroll_frame,
                text="No books found.",
                font=(SHARED_FONT_CUSTOM, 22),
                bg=SHARED_TABLE_BG_COLOR,
                fg=SHARED_SCROLLROW_TEXT_COLOR,
                pady=30,
            ).pack()
            return

        self._render_books_grid_or_list(
            canvas=canvas,
            scroll_frame=scroll_frame,
            books=books,
            sort_var=sort_var,
            view_var=view_var,
            view_btns=view_btns,
            context_label=context_label,
            panel_bg=SHARED_TABLE_BG_COLOR,
            cols=5,
            is_collection=False,
            collection_name=None,
            secondary_sort_var=secondary_sort_var,
            secondary_sort_reverse_var=secondary_sort_reverse_var,
        )

    # ---------- PAGE: TAG ----------
    def show_tag_page(self, tag_name: str):
        """Show all books with a specific tag."""
        self._show_filtered_books_page(
            page_type="tag",
            filter_value=tag_name,
        )
    def _filter_books_by_tag(self, tag_name: str) -> list[dict]:
        """Return all books that have the specified tag."""
        tag_lower = (tag_name or "").strip().lower()
        if not tag_lower:
            return []

        result = []
        for book in self.catalog:
            tags = book.get("tags")
            if isinstance(tags, list):
                # Check if any tag matches (case-insensitive)
                for t in tags:
                    if str(t).strip().lower() == tag_lower:
                        result.append(book)
                        break
        return result

    # ---------- PAGE: SEARCH RESULTS (merged with View All) ----------
    def show_search_results(self, results: list[dict], original_query: str = "", letter_filter: str | None = None, filter_field: str = "Title"):
        """
        Combined search results and view all books page.
        - If original_query is empty, shows all books with alphabet filter (formerly "View All")
        - If original_query has content, shows search results
        
        letter_filter: None = all results, 'A'-'Z' = starts with letter,
                       '#' = starts with number, '~' = starts with symbol
        filter_field: 'Title', 'Author (Last Name)', or 'Year' - which field to filter by
        """
        # Only call set_page if we're not suppressing (i.e., not during a back operation)
        if not getattr(self, "_nav_suppress_record", False):
            self.set_page("search_results", query=original_query, letter_filter=letter_filter, filter_field=filter_field)

        self.clear_page()
        self.set_background(SHOW_BOOKS_BG_IMG)
        self._page_img_refs.clear()

        # Determine heading text
        is_view_all = not original_query
        heading_text = "All Books" if is_view_all else f'Results for: "{original_query}"'

        # --- Top search row (entry fills space, button pinned right, centered) ---
        ROW_W = 700
        ROW_H = 35
        GAP = 0

        top_row = tk.Frame(self.canvas, bg=self.canvas.cget("bg"), highlightthickness=0, bd=0)
        top_row.place(relx=0.5, rely=0.08, anchor="n", width=ROW_W, height=ROW_H)
        top_row.pack_propagate(False)
        self.active_widgets.append(top_row)

        # 1) Create entry first (so search_entry exists)
        search_frame, search_entry = self.make_entry_bar(parent=top_row)

        # Force the entry container to fill height, and take the space left of the button.
        # (Your make_entry_bar already packs the Entry inside search_frame.)
        search_frame.configure(height=ROW_H)
        search_frame.pack_propagate(False)
        search_frame.pack(side="left", fill="both", expand=True, padx=(0, GAP))
        self.active_widgets.extend([search_frame, search_entry])

        # Optional: ensure the Entry itself has no OS highlight border
        search_entry.configure(bd=0, highlightthickness=0, relief="flat")

        # 2) Button pinned to the RIGHT (so it always stays aligned)
        search_btn = tk.Button(
            top_row,
            text="Search",
            command=lambda: self.perform_search(search_entry.get()),
            font=tkfont.Font(family=SHARED_FONT_CUSTOM, size=22),
            bg=SHARED_BUTTON1_BG_COLOR,
            fg=SHARED_BUTTON1_TEXT_COLOR,
            activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
            activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
            bd=0,
            highlightthickness=0,
            relief="flat",
            takefocus=False,
        )
        search_btn.pack(side="right", fill="y")  # right-anchored
        search_btn.configure(padx=0, pady=6)
        self.active_widgets.append(search_btn)

        # Pre-fill search entry with current query
        if original_query:
            search_entry.insert(0, original_query)

        def _do_search(_evt=None):
            self.perform_search(search_entry.get())
            return "break"

        search_entry.bind("<Return>", _do_search)
        search_entry.bind("<KP_Enter>", _do_search)

        self.update_idletasks()
        win_w = max(self.winfo_width(), 1)

        scale = max(1.0, min(1.35, win_w / 1280))
        title_size = int(round(90 * scale))
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=title_size, weight="bold")
        self._page_font_refs = getattr(self, "_page_font_refs", [])
        self._page_font_refs.append(title_font)

        self.make_canvas_text(
            heading_text,
            0.5,
            0.9,
            title_font,
        )

        self.mount_left_nav()

        # All books for counting (use results for search, full catalog for view all)
        all_books = results if not is_view_all else list(self.catalog)

        # Apply letter filter if set
        if letter_filter:
            filtered_books = [b for b in all_books if self._get_filter_first_char(b, filter_field) == letter_filter]
        else:
            filtered_books = all_books

        # Build context label
        if letter_filter:
            field_display = filter_field
            if filter_field == "Author (Last Name)":
                field_display = "Author"
            if letter_filter == "#":
                context = f"{heading_text} ({field_display}: 0-9)"
            elif letter_filter == "~":
                context = f"{heading_text} ({field_display}: Symbols)"
            else:
                context = f"{heading_text} ({field_display}: {letter_filter})"
        else:
            context = heading_text

        # Alphabet filter bar callback
        def on_filter_change(new_letter: str | None, new_field: str):
            self.show_search_results(
                results=results,
                original_query=original_query,
                letter_filter=new_letter,
                filter_field=new_field,
            )

        # Create alphabet bar - starts at rely=0.26
        alphabet_bar_rely = 0.15
        self._make_alphabet_filter_bar(
            books=all_books,
            filter_field=filter_field,
            letter_filter=letter_filter,
            on_filter_change=on_filter_change,
            show_filter_dropdown=True,
            rely=alphabet_bar_rely,
        )

        # Scroll container - position exactly below alphabet bar
        container, canvas, scroll_frame = self._make_scroll_container(
            bg=SHARED_TABLE_BG_COLOR,
            relwidth=0.88,
            relheight=0.60,
            top_inset=60,
        )

        # Position container so its top aligns exactly with bottom of alphabet bar
        container.place_configure(relx=0.5, rely=alphabet_bar_rely, y=36, anchor="n")
        self._raise_left_nav()
        self.after_idle(self._raise_left_nav)

        header = tk.Frame(container, bg=SHARED_MAINHEADER_BG_COLOR, height=60, highlightthickness=0, bd=0)
        header.place(x=0, y=0, relwidth=1.0, height=60)
        header.pack_propagate(False)
        self.active_widgets.append(header)

        sort_var, view_var, view_btns, secondary_sort_var, secondary_sort_reverse_var = self._make_sort_and_view_controls(
            header,
            bg=SHARED_MAINHEADER_BG_COLOR,
            pad_x=18,
            pad_y=10,
            default_view="list",
            default_sort="Title",
            sort_values=("Title", "Author", "Year")
        )

        if not filtered_books:
            tk.Label(
                scroll_frame,
                text="No books found.",
                font=(SHARED_FONT_CUSTOM, 22),
                bg=SHARED_TABLE_BG_COLOR,
                fg=SHARED_SCROLLROW_TEXT_COLOR,
                pady=30,
            ).pack()
            return

        self._render_books_grid_or_list(
            canvas=canvas,
            scroll_frame=scroll_frame,
            books=filtered_books,
            sort_var=sort_var,
            view_var=view_var,
            view_btns=view_btns,
            context_label=context,
            panel_bg=SHARED_TABLE_BG_COLOR,
            cols=5,
            is_collection=False,
            collection_name=None,
            secondary_sort_var=secondary_sort_var,
            secondary_sort_reverse_var=secondary_sort_reverse_var,
        )

    # ---------- PAGE: MANAGE LIB  ----------
    def gui_test_genres(self):
        try:
            stats = self.data.test_genre_lookup(sample_size=25, apply_and_save=True)
            self._refresh_catalog_from_data()
            messagebox.showinfo(
                "Genre test results",
                f"Tested: {stats['tested']}\n"
                f"Docs found: {stats['found_doc']}\n"
                f"Docs w/ subjects: {stats['got_subjects']}\n"
                f"Enriched & saved: {stats['enriched']}\n"
                f"Failed: {stats['failed']}\n\n"
                f"Total missing genre in catalog: {stats['total_missing_genre_in_catalog']}"
            )
        except Exception as e:
            messagebox.showerror("Genre test failed", str(e))
    def gui_scan_library(self):
        try:
            self.data.rebuild_queues()
            n_cover = len(self.data.sync_queue)
            n_genre = len(self.data.genre_queue)
            total = len(self.data.catalog)
            complete = total - len({*self.data.sync_queue, *self.data.genre_queue})
            messagebox.showinfo(
                "Library Scan Complete",
                f"Total books: {total}\n"
                f"Complete: {complete}\n"
                f"Missing covers: {n_cover}\n"
                f"Missing genres: {n_genre}"
            )
        except Exception as e:
            messagebox.showerror("Scan failed", str(e))
    def show_all_books_page(self):
        self.set_page("view_all")
        self.clear_page()
        self.set_background(SHOW_BOOKS_BG_IMG)
        self._page_img_refs.clear()

        self.update_idletasks()
        win_w = max(self.winfo_width(), 1)

        # Title scaling (matches your pattern)
        scale = max(1.0, min(1.35, win_w / 1280))
        title_size = int(round(60 * scale))
        title_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=title_size, weight="bold")

        self.make_canvas_text("All Books", relx=0.5, rely=0.16, font=title_font, fill="white")
        self.make_home_button()

        # Data
        books = list(self.catalog)

        # Scroll container (same as genre page)
        self._make_books_browser_card(
            panel_bg="#FFFFFF",
            header_h=60,
            context_label="All Books",
            books=books,
            cols=5, default_view="list",
        )

    # ---------- PAGE: BOOK DETAIL ----------
    def _book_detail_create_clickable_tags(self, *, tags_list: list, design_x: int, design_y: int,label_font, tag_font, S):
        """
        Create clickable tag chips on the book detail page.
        Clicking a tag opens the tag_page showing all books with that tag.
        """
        # Create a frame to hold the tags
        tags_frame = tk.Frame(self, bg=BOOKDETAIL_TAGDISPLAY_HOLDER_BG_COLOR, highlightthickness=0, bd=0)
        self.place_design(tags_frame, design_x, design_y, anchor="nw")
        self.active_widgets.append(tags_frame)

        # Store reference for hiding/showing
        self._book_detail_tags_frame = tags_frame
        self._book_detail_tags_frame_anchor = "nw"

        # "TAGS:" label
        tags_label = tk.Label(
            tags_frame,
            text="TAGS:",
            font=label_font,
            bg=BOOKDETAIL_TAGDISPLAY_HOLDER_BG_COLOR,
            fg=BOOKDETAIL_TAGDISPLAY_LABEL_TEXT_COLOR,
        )
        tags_label.pack(side="left", padx=(0, 8))
        self.active_widgets.append(tags_label)

        # Create clickable chips for each tag - limit to 4 tags to prevent overflow
        if tags_list:
            max_tags = 4
            shown_count = 0
            for tag in tags_list:
                if shown_count >= max_tags:
                    break
                tag_str = str(tag).strip()
                if not tag_str:
                    continue

                # Truncate long tag names to prevent running off page
                display_text = tag_str.upper() if len(tag_str) <= 20 else tag_str[:17].upper() + "..."

                chip = tk.Label(
                    tags_frame,
                    text=display_text,
                    font=tag_font,
                    bg=BOOKDETAIL_TAGDISPLAY_BG_COLOR,
                    fg=BOOKDETAIL_TAGDISPLAY_TEXT_COLOR,
                    padx=10,
                    pady=4,
                    cursor="hand2",
                )
                chip.pack(side="left", padx=(0, 6))
                self.active_widgets.append(chip)
                shown_count += 1

                # Bind click to open tag page (use full tag, not truncated)
                def _on_tag_click(e=None, t=tag_str):
                    self.show_tag_page(t)

                chip.bind("<Button-1>", _on_tag_click)

                # Hover effect
                def _on_enter(e, lbl=chip):
                    lbl.configure(bg=BOOKDETAIL_TAGDISPLAY_HOVER_BG_COLOR, fg=BOOKDETAIL_TAGDISPLAY_HOVER_TEXT_COLOR)
                def _on_leave(e, lbl=chip):
                    lbl.configure(bg=BOOKDETAIL_TAGDISPLAY_BG_COLOR, fg=BOOKDETAIL_TAGDISPLAY_TEXT_COLOR)
                chip.bind("<Enter>", _on_enter)
                chip.bind("<Leave>", _on_leave)

            # Show "+N more" if there are additional tags
            remaining = len([t for t in tags_list if str(t).strip()]) - shown_count
            if remaining > 0:
                more_label = tk.Label(
                    tags_frame,
                    text=f"+{remaining} more",
                    font=tag_font,
                    bg=BOOKDETAIL_TAGDISPLAY_HOLDER_BG_COLOR,
                    fg=BOOKDETAIL_TAGDISPLAY_SUB_TEXT_COLOR,
                )
                more_label.pack(side="left", padx=(4, 0))
                self.active_widgets.append(more_label)
        else:
            # Show "(no tags)" if empty
            no_tags = tk.Label(
                tags_frame,
                text="(none)",
                font=tag_font,
                bg=BOOKDETAIL_TAGDISPLAY_HOLDER_BG_COLOR,
                fg=BOOKDETAIL_TAGDISPLAY_SUB_TEXT_COLOR,
            )
            no_tags.pack(side="left")
            self.active_widgets.append(no_tags)
    def _book_detail_hide_tags_frame(self, hide: bool):
        """Hide or show the clickable tags frame."""
        frame = getattr(self, "_book_detail_tags_frame", None)
        if frame and frame.winfo_exists():
            if hide:
                frame.place_forget()
            else:
                # Re-place it (need to store position)
                pass  # Will be recreated on page refresh
    def _toggle_tags_editor(self, *, book: dict, plus_btn: tk.Button, design_x: int, design_y: int, S, BODY_FONT):
        """Toggles tag editor open/closed and swaps + <-> ✕ on the same button."""
        panel = getattr(self, "_tags_editor_panel", None)
        is_open = bool(panel and panel.winfo_exists())

        if is_open:
            # close - pass S and BODY_FONT for recreation
            self._book_detail_close_tags_editor(book=book, plus_btn=plus_btn, S=S, BODY_FONT=BODY_FONT)
        else:
            # open
            self._book_detail_open_tags_editor(
                book=book,
                plus_btn=plus_btn,
                design_x=design_x,
                design_y=design_y,
                S=S,
                BODY_FONT=BODY_FONT,
            )
    def _book_detail_close_tags_editor(self, *, book: dict, plus_btn: tk.Button, S=None, BODY_FONT=None):
        """Closes the editor panel and restores tags display + button to '+'."""
        panel = getattr(self, "_tags_editor_panel", None)
        if panel and panel.winfo_exists():
            try:
                panel.destroy()
            except Exception:
                pass
        self._tags_editor_panel = None

        # refresh tags from backend
        book_id = (book.get("book_id") or "").strip()
        try:
            tags = self.data.get_tags(book_id) if book_id else []
        except Exception:
            tags = book.get("tags") if isinstance(book.get("tags"), list) else []

        book["tags"] = tags
        self._refresh_catalog_from_data()

        # Destroy old tags frame
        old_frame = getattr(self, "_book_detail_tags_frame", None)
        if old_frame and old_frame.winfo_exists():
            try:
                old_frame.destroy()
            except Exception:
                pass

        # Recreate the clickable tags display with updated tags
        if S is None:
            win_w = max(self.winfo_width(), 1)
            scale = max(0.85, min(1.45, win_w / 1280))
            def S(px: int) -> int:
                return max(10, int(round(px * scale)))

        if BODY_FONT is None:
            try:
                fams = set(tkfont.families())
                BODY_FONT = "liberation-sans" if "liberation-sans" in fams else SHARED_FONT_CUSTOM
            except Exception:
                BODY_FONT = SHARED_FONT_CUSTOM

        # Get card position for tags placement
        CARD_X, CARD_Y = 840, 460
        CARD_W, CARD_H = 640, 320
        pad_x = 20
        card_left = CARD_X - (CARD_W // 2)
        TAGS_X = card_left + pad_x
        TAGS_Y = 650

        tags_label_font = (BODY_FONT, S(16), "bold")
        tags_font = (BODY_FONT, S(13))

        self._book_detail_create_clickable_tags(
            tags_list=tags,
            design_x=TAGS_X,
            design_y=TAGS_Y,
            label_font=tags_label_font,
            tag_font=tags_font,
            S=S,
        )
        self._book_detail_tags = {
            "x": TAGS_X,
            "y": TAGS_Y,
        }

        try:
            plus_btn.config(text="+")
        except Exception:
            pass
        try:
            cmd = getattr(plus_btn, "_toggle_cmd", None)
            if cmd:
                plus_btn.config(command=cmd)
        except Exception:
            pass
    def _book_detail_set_tags_canvas(self, *, text: str, design_x: int, design_y: int, font, fill: str = THEME_COLOR2, wrap_w: int | None = None, right_pad: int = 24, ):
        """Create/update a canvas text item for TAGS (left-aligned + wrapped)."""
        info = getattr(self, "_book_detail_tags", None)

        x_px, y_px = self._design_to_real_xy(design_x, design_y)

        # If caller didn't specify, default to a reasonable width
        desired = int(wrap_w) if wrap_w is not None else 520

        # Clamp so we NEVER run off the window to the right
        max_fit = max(self.winfo_width() - x_px - right_pad, 120)
        wrap_px = max(120, min(desired, max_fit))

        if not info or not self.canvas.type(info.get("item")):
            item = self.canvas.create_text(
                x_px, y_px,
                text=text,
                fill=fill,
                font=font,
                anchor="nw",
                justify="left",
                width=wrap_px,  # ✅ wrapping happens here
                tags=("ui_text",),
            )
            self._book_detail_tags = {
                "item": item,
                "x": design_x,
                "y": design_y,
                "wrap_w": desired,  # ✅ store desired width for resize
                "right_pad": right_pad,
            }
        else:
            item = info["item"]
            self.canvas.itemconfigure(item, text=text, font=font, fill=fill, width=wrap_px)
            self.canvas.coords(item, x_px, y_px)
            info["x"], info["y"] = design_x, design_y
            info["wrap_w"] = desired
            info["right_pad"] = right_pad
    def _book_detail_hide_tags_canvas(self, hide: bool):
        info = getattr(self, "_book_detail_tags", None)
        if not info:
            return
        try:
            self.canvas.itemconfigure(info["item"], state=("hidden" if hide else "normal"))
        except Exception:
            pass
    def _book_detail_open_tags_editor(self, *, book: dict, plus_btn: tk.Button, design_x: int, design_y: int, S,BODY_FONT):
        """
        Edit mode overlay:
        - hides TAGS canvas text
        - shows Entry with autocomplete suggestions
        - shows tag chips with ✕ remove
        design_x/design_y = TOP-LEFT of the "+" button (design coords)
        """
        book_id = (book.get("book_id") or "").strip()
        if not book_id:
            return

        existing = getattr(self, "_tags_editor_panel", None)
        if existing and existing.winfo_exists():
            return

        self._book_detail_hide_tags_canvas(True)

        # Also hide the clickable tags frame
        tags_frame = getattr(self, "_book_detail_tags_frame", None)
        if tags_frame and tags_frame.winfo_exists():
            tags_frame.place_forget()

        # swap button to ✕ while open
        try:
            plus_btn.config(text="✕")
        except Exception:
            pass

        # place editor to the RIGHT of the button
        PLUS_W = 34
        GAP = 10
        editor_x = design_x + PLUS_W + GAP
        editor_y = design_y
        PLUS_Y = design_y + 4

        panel = tk.Frame(
            self,
            bg=BOOKDETAIL_TAGHOLDER_BG_COLOR,
            highlightthickness=1,
            highlightbackground=BOOKDETAIL_TAGHOLDER_BORDER_COLOR,
            bd=0
        )
        self.place_design(panel, editor_x, editor_y, anchor="nw")
        self.active_widgets.append(panel)
        self._tags_editor_panel = panel

        header = tk.Frame(panel, bg=BOOKDETAIL_TAGHOLDER_BG_COLOR, bd=0, highlightthickness=0)
        header.pack(fill="x", padx=10, pady=8)

        entry = tk.Entry(
            header,
            font=(BODY_FONT, S(14)),
            bg=THEME_COLOR2,
            fg=BOOKDETAIL_TAGENTRY_TEXT_COLOR,
            insertbackground=THEME_COLOR2,
            relief="solid",
            bd=1,
            highlightthickness=0,
            width=26,
        )
        entry.pack(side="left")
        entry.focus_set()
        self.active_widgets.append(entry)

        # Suggestions frame (below entry) - wrapping layout handles overflow
        suggestions_frame = tk.Frame(panel, bg=BOOKDETAIL_TAGHOLDER_BG_COLOR, bd=0, highlightthickness=0)
        suggestions_frame.pack(fill="x", padx=10, pady=(0, 5))
        self.active_widgets.append(suggestions_frame)

        chips = tk.Frame(panel, bg=BOOKDETAIL_TAGSELECT_HOLDER_BG_COLOR, bd=0, highlightthickness=0)
        chips.pack(fill="both", padx=10, pady=(0, 10))
        self.active_widgets.append(chips)

        def split_user_tags(raw: str) -> list[str]:
            if not raw:
                return []
            parts = re.split(r"[,\n;]+", raw)
            return [p.strip() for p in parts if p and p.strip()]

        def get_all_tags_in_library() -> set[str]:
            """Get all unique tags from all books in the catalog."""
            all_tags = set()
            for b in self.catalog:
                book_tags = b.get("tags")
                if isinstance(book_tags, list):
                    for t in book_tags:
                        tag_str = str(t).strip().lower()
                        if tag_str:
                            all_tags.add(tag_str)
            return all_tags

        def get_recent_tags(limit: int = 3) -> list[str]:
            """Get the most recently added tags (stored in instance)."""
            recent = getattr(self, "_recent_tags_added", [])
            return recent[:limit]

        def add_to_recent_tags(tags: list[str]):
            """Add tags to the recent tags list."""
            recent = getattr(self, "_recent_tags_added", [])
            for t in reversed(tags):
                t_lower = t.strip().lower()
                if t_lower:
                    # Remove if already exists (to move to front)
                    recent = [r for r in recent if r.lower() != t_lower]
                    recent.insert(0, t_lower)
            # Keep only last 10
            self._recent_tags_added = recent[:10]

        def update_suggestions(event=None):
            for child in suggestions_frame.winfo_children():
                child.destroy()

            current_text = entry.get().strip().lower()

            try:
                book_tags = self.data.get_tags(book_id)
            except Exception:
                book_tags = book.get("tags") if isinstance(book.get("tags"), list) else []
            current_tags = {str(t).strip().lower() for t in book_tags}

            # ---- NEW: suggestions come from backend "recent tags" ----
            try:
                recent = self.data.get_recent_tags_global(50)  # grab more so filtering still yields up to 6
            except Exception:
                recent = []

            # Build list in priority order:
            # 1) recent tags (most recent first)
            # 2) remaining tags in library (alphabetical), as fallback for typed searching
            all_tags = sorted(get_all_tags_in_library())
            ordered = []
            seen = set()

            for t in recent:
                if t and t not in seen:
                    ordered.append(t)
                    seen.add(t)

            for t in all_tags:
                t = str(t).strip().lower()
                if t and t not in seen:
                    ordered.append(t)
                    seen.add(t)

            # Filter by empty/typed input + exclude tags already on this book
            suggestions = []
            if not current_text:
                for t in get_recent_tags(6):  # <-- you said last 6
                    if t.lower() not in current_tags:
                        suggestions.append(t)
                        if len(suggestions) >= 6:
                            break
            else:
                for t in sorted(get_all_tags_in_library()):
                    if current_text in t.lower() and t.lower() not in current_tags:
                        suggestions.append(t)
                        if len(suggestions) >= 6:
                            break

            if not suggestions:
                if suggestions_frame.winfo_manager():  # it's currently packed/managed
                    suggestions_frame.pack_forget()
                    panel.update_idletasks()
                return

            if not suggestions_frame.winfo_manager():
                suggestions_frame.pack(fill="x", padx=10, pady=(0, 5), before=chips)

            # ---- your existing layout code below stays the same ----
            panel.update_idletasks()
            available_width = panel.winfo_width() - 20
            if available_width < 120:
                available_width = S(520)

            current_row = tk.Frame(suggestions_frame, bg=BOOKDETAIL_TAGHOLDER_BG_COLOR, bd=0, highlightthickness=0)
            current_row.pack(fill="x", anchor="w")

            sug_label = tk.Label(
                current_row,
                text="Suggestions:",
                bg=BOOKDETAIL_TAGHOLDER_BG_COLOR,
                fg=BOOKDETAIL_TAGHOLDER_SUBTEXT_COLOR,
                font=(BODY_FONT, S(11)),
            )
            sug_label.pack(side="left", padx=(0, 5))
            sug_label.update_idletasks()
            current_row_width = sug_label.winfo_reqwidth() + 5

            for sug in suggestions:
                sug_btn = tk.Label(
                    current_row,
                    text=sug,
                    bg=BOOKDETAIL_TAGSUGGEST_BG_COLOR,
                    fg=BOOKDETAIL_TAGSUGGEST_TEXT_COLOR,
                    font=(BODY_FONT, S(12)),
                    padx=8,
                    pady=2,
                    cursor="hand2",
                )
                sug_btn.update_idletasks()
                btn_width = sug_btn.winfo_reqwidth() + 4

                if current_row_width + btn_width > available_width and current_row_width > sug_label.winfo_reqwidth() + 10:
                    current_row = tk.Frame(suggestions_frame, bg=BOOKDETAIL_TAGHOLDER_BG_COLOR, bd=0, highlightthickness=0)
                    current_row.pack(fill="x", anchor="w", pady=(2, 0))
                    current_row_width = 0
                    sug_btn.destroy()
                    sug_btn = tk.Label(
                        current_row,
                        text=sug,
                        bg=BOOKDETAIL_TAGSUGGEST_BG_COLOR,
                        fg=BOOKDETAIL_TAGSUGGEST_TEXT_COLOR,
                        font=(BODY_FONT, S(12)),
                        padx=8,
                        pady=2,
                        cursor="hand2",
                    )

                sug_btn.pack(side="left", padx=2)
                current_row_width += btn_width

                def _add_suggestion(e=None, tag=sug):
                    try:
                        self.data.add_tags(book_id, [tag], persist=True)  # backend will update recent history
                    except Exception:
                        tags = book.get("tags") if isinstance(book.get("tags"), list) else []
                        if tag.lower() not in {str(x).strip().lower() for x in tags}:
                            tags.append(tag)
                        book["tags"] = tags

                    self._refresh_catalog_from_data()
                    entry.delete(0, "end")
                    refresh_chips()
                    update_suggestions()

                sug_btn.bind("<Button-1>", _add_suggestion)

                def _on_enter(e, lbl=sug_btn):
                    lbl.configure(bg=BOOKDETAIL_TAGSUGGEST_HOVER_BG_COLOR, fg=BOOKDETAIL_TAGSUGGEST_HOVER_TEXT_COLOR)

                def _on_leave(e, lbl=sug_btn):
                    lbl.configure(bg=BOOKDETAIL_TAGSUGGEST_BG_COLOR, fg=BOOKDETAIL_TAGSUGGEST_TEXT_COLOR)

                sug_btn.bind("<Enter>", _on_enter)
                sug_btn.bind("<Leave>", _on_leave)

        def refresh_chips():
            for child in chips.winfo_children():
                child.destroy()

            try:
                tags = self.data.get_tags(book_id)
            except Exception:
                tags = book.get("tags") if isinstance(book.get("tags"), list) else []

            max_cols = 6
            r = 0
            c = 0

            if not tags:
                tk.Label(
                    chips,
                    text="(no tags yet)",
                    bg=BOOKDETAIL_TAGSELECT_HOLDER_BG_COLOR,
                    fg=BOOKDETAIL_NOTAGS_TEXT_COLOR,
                    font=(BODY_FONT, S(13)),
                ).grid(row=0, column=0, sticky="w")
                return

            for t in tags:
                chip = tk.Frame(chips, bg=THEME_COLOR2, bd=0, highlightthickness=0)
                chip.grid(row=r, column=c, padx=6, pady=6, sticky="w")

                tk.Label(
                    chip,
                    text=str(t),
                    bg=BOOKDETAIL_TAGSELECT_BG_COLOR,
                    fg=BOOKDETAIL_TAGENTRY_TEXT_COLOR,
                    font=(BODY_FONT, S(13)),
                    padx=8,
                    pady=4,
                ).pack(side="left")

                X_SIZE = S(18)
                BORDER = BOOKDETAIL_TAGEDIT_XBTN_BORDER_COLOR

                xwrap = tk.Frame(chip, width=X_SIZE, height=X_SIZE, bg=BORDER, highlightthickness=0, bd=0)
                xwrap.pack_propagate(False)
                xwrap.pack(side="left", padx=(2, 6), pady=2)

                # inner wrapper = the white face (creates a 1px border by padding)
                inner = tk.Frame(xwrap, bg=SHARED_BUTTON2_BG_COLOR, highlightthickness=0, bd=0)
                inner.pack(fill="both", expand=True, padx=1, pady=1)

                # clickable X (Label instead of Button to avoid macOS bevel/top line)
                xbtn = tk.Label(
                    inner,
                    text="✕",
                    bg=BOOKDETAIL_TAGEDIT_XBTN_BG_COLOR,
                    fg=BOOKDETAIL_TAGEDIT_XSYMBOL_COLOR,
                    font=(BODY_FONT, S(10), "bold"),
                    cursor="hand2",
                )
                xbtn.pack(fill="both", expand=True)

                xbtn.bind("<Button-1>", lambda e, tag=t: (remove_tag(tag), "break"))

                self.active_widgets.extend([xwrap, inner, xbtn])

                c += 1
                if c >= max_cols:
                    c = 0
                    r += 1

        def add_from_entry(_evt=None):
            raw = entry.get().strip()
            if not raw:
                return "break"
            entry.delete(0, "end")

            items = split_user_tags(raw)
            if not items:
                return "break"

            try:
                self.data.add_tags(book_id, items, persist=True)
                add_to_recent_tags(items)
            except Exception:
                tags = book.get("tags") if isinstance(book.get("tags"), list) else []
                low = {str(x).strip().lower() for x in tags}
                for it in items:
                    if it.strip().lower() not in low:
                        tags.append(it.strip().lower())
                book["tags"] = tags

            self._refresh_catalog_from_data()
            refresh_chips()
            update_suggestions()
            return "break"

        def remove_tag(tag: str):
            try:
                self.data.remove_tag(book_id, tag, persist=True)
            except Exception:
                tags = book.get("tags") if isinstance(book.get("tags"), list) else []
                norm = str(tag).strip().lower()
                book["tags"] = [t for t in tags if str(t).strip().lower() != norm]
            self._refresh_catalog_from_data()
            refresh_chips()
            update_suggestions()

        entry.bind("<Return>", add_from_entry)
        entry.bind("<KeyRelease>", update_suggestions)
        entry.bind("<FocusIn>", update_suggestions)
        
        refresh_chips()
        update_suggestions()  # Show recent tags initially
    def _mount_tags_editor_strip(self, *, book: dict, initial_tags: list[str], S, BODY_FONT):
        """
        Creates a Tags UI strip near the bottom of the book info page:
        - Always shows a "+" button
        - Clicking "+" opens an Entry + Done button
        - When open, each tag shows an "x" button to remove it
        - Press Return in entry to add (supports comma/semicolon/newline separated)
        """

        book_id = (book.get("book_id") or "").strip()
        if not book_id:
            return  # nothing to edit

        # --- state ---
        state = {
            "editing": False,
            "tags": [t for t in (initial_tags or []) if str(t).strip()],
        }

        # --- container pinned using your design placement system ---
        panel = tk.Frame(self, bg=THEME_COLOR2, highlightthickness=0, bd=0)
        # near where you used relx=0.5, rely=0.9 (≈ y=648 in 720 design)
        self.place_design(panel, 640, 655, anchor="center")
        self.active_widgets.append(panel)

        # small consistent fonts
        lbl_font = (BODY_FONT, S(16), "bold")
        tag_font = (BODY_FONT, S(14))
        btn_font = (BODY_FONT, S(14), "bold")

        def _split_user_tags(raw: str) -> list[str]:
            if not raw:
                return []
            parts = re.split(r"[,\n;]+", raw)
            out = []
            for p in parts:
                t = (p or "").strip()
                if t:
                    out.append(t)
            return out

        def _refresh_tags_from_backend():
            # pull from backend as source of truth
            try:
                tags = self.data.get_tags(book_id)
            except Exception:
                tags = state["tags"]

            state["tags"] = tags
            book["tags"] = tags  # keep local dict in sync
            self._refresh_catalog_from_data()

        def _render():
            # clear panel content only (don’t clear the page)
            for child in panel.winfo_children():
                child.destroy()

            # --- HEADER ROW (TAGS + button + optional entry) ---
            header = tk.Frame(panel, bg=THEME_COLOR2, highlightthickness=0, bd=0)
            header.pack(fill="x", padx=12, pady=(10, 6))

            tk.Label(
                header,
                text="TAGS:",
                bg=BOOKDETAIL_TAGSELECT_HOLDER_BG_COLOR,
                fg=BOOKDETAIL_TAGHOLDER_SUBTEXT_COLOR,
                font=lbl_font
            ).pack(side="left", padx=(0, 10))

            # toggle + / ✕
            plus_btn = tk.Button(
                header,
                text=("✕" if state["editing"] else "+"),
                command=(lambda: _close_editor() if state["editing"] else _open_editor()),
                bg=BOOKDETAIL_TAGSELECT_HOLDER_BG_COLOR,
                fg=BOOKDETAIL_TAGHOLDER_SUBTEXT_COLOR,
                activebackground=SHARED_ALPHABAR_BG_COLOR,
                activeforeground=SHARED_ALPHA_HOVER_TEXT_COLOR,
                bd=0,
                highlightthickness=0,
                relief="flat",
                takefocus=False,
                font=btn_font,
                padx=12,
                pady=2,
            )
            plus_btn.pack(side="left", padx=(0, 10))
            self.active_widgets.append(plus_btn)

            entry = None
            if state["editing"]:
                entry = tk.Entry(
                    header,
                    font=(BODY_FONT, S(14)),
                    bg=SHARED_ALPHA_MUTED_BG_COLOR,
                    fg=SHARED_ALPHA_MUTED_TEXT_COLOR,
                    insertbackground=SHARED_ENTRY2_CURSOR_COLOR,
                    relief="flat",
                    bd=1,
                    highlightthickness=0,
                    width=28,
                )
                entry.pack(side="left")
                entry.focus_set()
                self._style_entry(entry)
                self.active_widgets.append(entry)

                def _submit(_evt=None):
                    raw = entry.get()
                    entry.delete(0, "end")
                    items = _split_user_tags(raw)
                    if not items:
                        return "break"
                    try:
                        self.data.add_tags(book_id, items, persist=True)
                    except Exception:
                        # fallback: update local state only
                        low = {str(x).strip().lower() for x in state["tags"]}
                        for it in items:
                            itn = it.strip().lower()
                            if itn and itn not in low:
                                state["tags"].append(itn)
                                low.add(itn)
                        book["tags"] = state["tags"]

                    _refresh_tags_from_backend()
                    _render()
                    return "break"

                entry.bind("<Return>", _submit)

            # --- CHIPS AREA (FLOW WRAP, pixel-based) ---
            chips_area = tk.Frame(panel, bg=THEME_COLOR2, highlightthickness=0, bd=0)
            chips_area.pack(fill="x", padx=12, pady=(0, 12))
            chips_area.pack_propagate(False)  # we set its height after layout
            self.active_widgets.append(chips_area)

            gap_x = 10
            gap_y = 10

            def _layout_chips(chip_widgets: list[tk.Widget]):
                max_w = chips_area.winfo_width()
                if max_w <= 2:
                    chips_area.after(16, lambda: _layout_chips(chip_widgets))
                    return

                x = 0
                y = 0
                row_h = 0

                for w in chip_widgets:
                    w.update_idletasks()
                    cw = w.winfo_reqwidth()
                    ch = w.winfo_reqheight()

                    # wrap to next line if chip would overflow
                    if x > 0 and (x + cw) > max_w:
                        x = 0
                        y += row_h + gap_y
                        row_h = 0

                    w.place(x=x, y=y)
                    x += cw + gap_x
                    row_h = max(row_h, ch)

                chips_area.configure(height=y + row_h)

            def _build_chip(tag: str) -> tk.Frame:
                # Ellipsize long tags so one chip can’t blow up layout
                tag_font_obj = tkfont.Font(family=BODY_FONT, size=S(13))
                max_w = max(chips_area.winfo_width(), 1)
                max_text_px = max(max_w - S(64), S(140))  # padding + X box room
                tag_txt = self._ellipsize_px(str(tag), tag_font_obj, max_text_px)

                chip = tk.Frame(chips_area, bg=BOOKDETAIL_TAGEDIT_XBTN_BORDER_COLOR, bd=0, highlightthickness=0)

                tk.Label(
                    chip,
                    text=tag_txt,
                    bg=BOOKDETAIL_TAGEDIT_XBTN_BG_COLOR,
                    fg=BOOKDETAIL_TAGEDIT_SYMBOL_COLOR,
                    font=(BODY_FONT, S(13)),
                    padx=10,
                    pady=6,
                ).pack(side="left")

                if state["editing"]:
                    # ✅ size from your first snippet
                    X_SIZE = S(18)

                    # ✅ thin flat grey border, no bevel (use a Label as the clickable control)
                    xwrap = tk.Frame(
                        chip,
                        width=X_SIZE,
                        height=X_SIZE,
                        bg=SHARED_MAINHEADER_BG_COLOR,
                        highlightthickness=1,
                        highlightbackground=SHARED_RADIO_TEXT_COLOR,
                        bd=0,
                    )
                    xwrap.pack_propagate(False)
                    xwrap.pack(side="left", padx=(6, 8), pady=4)

                    xlbl = tk.Label(
                        xwrap,
                        text="✕",
                        bg=SHARED_XBTN_BG_COLOR,
                        fg=SHARED_XBTN_SELECTED_ONCLICK_COLOR,
                        font=(BODY_FONT, S(10), "bold"),
                        cursor="hand2",
                    )
                    xlbl.pack(fill="both", expand=True)

                    # click removes
                    xlbl.bind("<Button-1>", lambda e, t=tag: (_remove_tag(t), "break"))

                    self.active_widgets.extend([xwrap, xlbl])

                self.active_widgets.append(chip)
                return chip

            # clear old chip children (we rebuild every render)
            for child in chips_area.winfo_children():
                child.destroy()

            if not state["tags"]:
                empty = tk.Label(
                    chips_area,
                    text="(no tags yet)",
                    bg=BOOKDETAIL_TAGSELECT_HOLDER_BG_COLOR,
                    fg=EDITCOLL_SUBTEXT_COLOR,
                    font=tag_font,
                )
                empty.place(x=0, y=0)
                chips_area.configure(height=S(26))
                self.active_widgets.append(empty)
                return

            chip_widgets = [_build_chip(t) for t in state["tags"]]
            _layout_chips(chip_widgets)

            # re-flow on resize (debounced)
            def _on_chips_resize(_evt=None):
                after_id = getattr(self, "_tags_wrap_after_id", None)
                if after_id:
                    try:
                        self.after_cancel(after_id)
                    except Exception:
                        pass
                self._tags_wrap_after_id = self.after(40, lambda: _layout_chips(chip_widgets))

            chips_area.bind("<Configure>", _on_chips_resize)

        def _open_editor():
            state["editing"] = True
            _render()

        def _close_editor():
            state["editing"] = False
            _render()

        def _remove_tag(tag: str):
            try:
                self.data.remove_tag(book_id, tag, persist=True)
            except Exception:
                norm = tag.strip().lower()
                state["tags"] = [t for t in state["tags"] if str(t).strip().lower() != norm]
                book["tags"] = state["tags"]
            _refresh_tags_from_backend()
            _render()

        # initial sync + render
        _refresh_tags_from_backend()
        _render()
    def show_book_detail(self, book: dict):
        self.set_page("book_detail", book=book)
        self._current_book_detail = book
        self.clear_page()
        self.set_background(BOOK_INFO_BG_IMG)
        self._page_img_refs.clear()

        edit_mode = bool(getattr(self, "_book_edit_mode", False))
        if not edit_mode:

            def _do_search(_evt=None):
                self.perform_search(search_entry.get())
                return "break"

            # --- Top search row (entry fills space, button pinned right, centered) ---
            ROW_W = 700
            ROW_H = 35
            GAP = 0

            top_row = tk.Frame(self.canvas, bg=self.canvas.cget("bg"), highlightthickness=0, bd=0)
            top_row.place(relx=0.5, rely=0.08, anchor="n", width=ROW_W, height=ROW_H)
            top_row.pack_propagate(False)
            self.active_widgets.append(top_row)

            # 1) Create entry first (so search_entry exists)
            search_frame, search_entry = self.make_entry_bar(parent=top_row)

            # Force the entry container to fill height, and take the space left of the button.
            # (Your make_entry_bar already packs the Entry inside search_frame.)
            search_frame.configure(height=ROW_H)
            search_frame.pack_propagate(False)
            search_frame.pack(side="left", fill="both", expand=True, padx=(0, GAP))
            self.active_widgets.extend([search_frame, search_entry])

            # Optional: ensure the Entry itself has no OS highlight border
            search_entry.configure(bd=0, highlightthickness=0, relief="flat")

            # 2) Button pinned to the RIGHT (so it always stays aligned)
            search_btn = tk.Button(
                top_row,
                text="Search",
                command=lambda: self.perform_search(search_entry.get()),
                font=tkfont.Font(family=SHARED_FONT_CUSTOM, size=20),
                bg=SHARED_BUTTON1_BG_COLOR,
                fg=SHARED_BUTTON1_TEXT_COLOR,
                activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
                activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
                bd=0,
                highlightthickness=0,
                relief="flat",
                takefocus=False,
            )
            search_btn.pack(side="right", fill="y")  # right-anchored
            search_btn.configure(padx=0, pady=6)
            self.active_widgets.append(search_btn)
        # ---------- pull fields ----------
        title = self._unescape_entities(book.get("title") or "Untitled")

        first = (book.get("first_name") or "").strip()
        last = (book.get("last_name") or "").strip()
        creators = (book.get("creators") or "").strip()
        author = f"{first} {last}".strip() if (first or last) else (creators or "Unknown author")

        genre = (book.get("genre") or "").strip() or "Genre"
        raw_tags = book.get("tags")

        if isinstance(raw_tags, list):
            tags_list = [str(t).strip() for t in raw_tags if str(t).strip()]
        elif isinstance(raw_tags, str):
            # allow legacy string like "historical romance, vampires"
            tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
        else:
            tags_list = []

        desc = (book.get("description") or book.get("notes") or "").strip() or "No description available."
        # Decode HTML entities like &#039; -> ' (sometimes double-escaped)
        for _ in range(2):
            new = html.unescape(desc)
            if new == desc:
                break
            desc = new

        isbn = str(
            book.get("isbn")
            or book.get("ISBN")
            or book.get("ean_isbn13")
            or book.get("upc_isbn10")
            or ""
        ).strip()

        # ---------- scale ----------
        self.update_idletasks()
        win_w = max(self.winfo_width(), 1)
        scale = max(0.85, min(1.45, win_w / 1280))

        # S = for layout + genre (allowed to grow)
        def S(px: int) -> int:
            return max(10, int(round(px * scale)))

        # T = for description-card text (DO NOT grow past 1.0)
        text_scale = min(scale, 1.0)

        def T(px: int) -> int:
            return max(10, int(round(px * text_scale)))

        # ---------- fonts ----------
        try:
            fams = set(tkfont.families())
            BODY_FONT = "liberation-sans" if "liberation-sans" in fams else SHARED_FONT_CUSTOM
        except Exception:
            BODY_FONT = SHARED_FONT_CUSTOM

        # ---------- layout constants ----------
        # Base (windowed) layout
        fs = bool(self._is_fullscreen_like())
        pad_x, pad_y = 20, 12

        COVER_X = 330
        ISBN_Y = 620
        COVER_W, COVER_H = 260, 380
        COVER_GAP = 25

        CARD_X, CARD_Y = 840, 460
        CARD_W, CARD_H = 640, 320

        # Fine-tune pinned text blocks relative to the card
        GENRE_Y_RAISE = 0  # negative = up
        TAGS_Y_DROP = 0  # positive = down

        if fs:
            ISBN_Y = 620 + S(30)  # ✅ MUST MATCH show_book_detail
            COVER_X = 210
            CARD_X = 920
            CARD_W = 820
            CARD_H = 420
            GENRE_Y_RAISE = 0
            TAGS_Y_DROP = S(18)

        self._book_detail_layout = {
            "CARD_X": CARD_X, "CARD_Y": CARD_Y,
            "CARD_W": CARD_W, "CARD_H": CARD_H,
            "pad_x": pad_x,
            "GENRE_GAP": S(10),  # tweak spacing here
        }
        desc_top = pad_y + S(72)


        # --- genre (canvas text, pinned to card left) ---
        genre_clean = (genre or "").strip()
        if genre_clean and genre_clean.lower() != "genre":
            genre_clean = genre_clean.title()

            genre_font = tkfont.Font(
                family=SHARED_FONT_CUSTOM,
                size=S(52),
                weight="bold"
            )
            self._book_detail_genre_font = genre_font
            self._page_font_refs = getattr(self, "_page_font_refs", [])
            self._page_font_refs.append(genre_font)

            card_left = CARD_X - (CARD_W // 2)
            card_top = CARD_Y - (CARD_H // 2)

            genre_x_design = card_left + pad_x
            GENRE_GAP = S(10)  # spacing between text and card edge
            genre_h_px = int(genre_font.metrics("linespace"))
            genre_h_design = int(round(genre_h_px / scale))
            genre_y_design = card_top - genre_h_design - GENRE_GAP

            # Create it once in the right place (pixels)
            x_px, y_px = self._design_to_real_xy(genre_x_design, genre_y_design)
            genre_item = self.canvas.create_text(
                x_px, y_px,
                text=genre_clean,
                fill=THEME_COLOR2,
                font=genre_font,
                anchor="nw",
                justify="left"
            )

            # Store info so we can reposition it on resize
            self._book_detail_genre = {
                "item": genre_item,
                "x": genre_x_design,
                "y": genre_y_design,
            }

        # ---------- TAGS (clickable chips) ----------
        tags_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=S(18))
        tags_label_font = tkfont.Font(family=SHARED_FONT_CUSTOM, size=S(20), weight="bold")

        # Align TAGS with the description box left edge
        card_left = CARD_X - (CARD_W // 2)
        TAGS_X = card_left + pad_x
        TAGS_Y = 650 + (S(22) if fs else 0) + TAGS_Y_DROP
        PLUS_W = 34
        PLUS_H = 34
        PLUS_GAP = 10  # space between + and tags
        PLUS_X = TAGS_X - PLUS_W - PLUS_GAP
        PLUS_Y = TAGS_Y  # align top with tags row

        if not getattr(self, "_book_edit_mode", False):
            # Create clickable tag chips row
            self._book_detail_create_clickable_tags(
                tags_list=tags_list,
                design_x=TAGS_X,
                design_y=TAGS_Y,
                label_font=tags_label_font,
                tag_font=tags_font,
                S=S,
            )
            self._book_detail_tags = {"x": TAGS_X, "y": TAGS_Y}

            # + button frame
            plus_frame = tk.Frame(self, width=PLUS_W, height=PLUS_H, bg=SHARED_PLUSBTN_BG_COLOR, highlightthickness=0,
                                  bd=0)
            plus_frame.pack_propagate(False)

            self.place_design(plus_frame, PLUS_X, PLUS_Y, anchor="nw")
            self.active_widgets.append(plus_frame)
            self._book_detail_plus_frame = plus_frame
            self._book_detail_plus_anchor = "nw"

            plus_x_design = PLUS_X
            plus_y_design = PLUS_Y

            plus_btn = tk.Button(
                plus_frame,
                text="+",
                command=lambda b=book, pb=None: None,
                bg=BOOKDETAIL_TAGEDIT_SYMBOL_ONCLICK_COLOR,
                fg=BOOKDETAIL_TAGEDIT_SYMBOL_COLOR,
                activebackground=BOOKDETAIL_TAGHOLDER_SUBTEXT_COLOR,
                activeforeground=BOOKDETAIL_TAGEDIT_SYMBOL_ONCLICK_COLOR,
                bd=0,
                highlightthickness=0,
                relief="flat",
                takefocus=False,
                font=(BODY_FONT, S(16), "bold"),
            )
            plus_btn.pack(fill="both", expand=True)
            self.active_widgets.append(plus_btn)

            toggle_cmd = lambda b=book, pb=plus_btn, px=plus_x_design, py=plus_y_design: self._toggle_tags_editor(
                book=b, plus_btn=pb, design_x=px, design_y=py, S=S, BODY_FONT=BODY_FONT
            )
            plus_btn._toggle_cmd = toggle_cmd  # type: ignore[attr-defined]
            plus_btn.config(command=toggle_cmd)

        else:
            # If switching into edit mode, make sure any old tags UI is not left visible
            old_frame = getattr(self, "_book_detail_tags_frame", None)
            if old_frame and old_frame.winfo_exists():
                try:
                    old_frame.destroy()
                except Exception:
                    pass
            self._book_detail_tags_frame = None

            old_plus = getattr(self, "_book_detail_plus_frame", None)
            if old_plus and old_plus.winfo_exists():
                try:
                    old_plus.destroy()
                except Exception:
                    pass
            self._book_detail_plus_frame = None

            # If you ever created canvas text tags on this page, hide them too:
            try:
                self._book_detail_hide_tags_canvas(True)
            except Exception:
                pass
        # ---------- ISBN (anchor first) ----------
        if isbn:
            isbn_lbl = tk.Label(
                self,
                text=f"ISBN: {isbn}",
                bg=BOOKDETAIL_ISBN_BG_COLOR,
                fg=BOOKDETAIL_ISBN_TEXT_COLOR,
                font=(BODY_FONT, S(12)),
                bd=0,
                highlightthickness=0
            )
            self.place_design(isbn_lbl, COVER_X, ISBN_Y, anchor="s")
            self.active_widgets.append(isbn_lbl)
            self._book_detail_isbn_lbl = isbn_lbl
            self._book_detail_isbn_anchor = "s"

        # ---------- cover (stacked above ISBN) ----------
        book_id = (book.get("book_id") or "").strip()
        cover_path = self.data.get_cover_path(book_id) if book_id else None

        # ---------- cover (center-align with card) ----------
        book_id = (book.get("book_id") or "").strip()
        cover_path = self.data.get_cover_path(book_id) if book_id else None

        # We want: cover CENTER Y == CARD_Y (design coords)
        # Since we place with anchor="s" (bottom), bottom_y = center_y + (height/2)
        # BUT: image heights are in real pixels, so convert to design-units using your scale.
        def _px_to_design(px: int) -> int:
            return int(round(px / scale))  # scale already defined above

        display_w_px = COVER_W
        display_h_px = COVER_H

        if cover_path and cover_path.exists():
            pil = Image.open(cover_path).convert("RGB")
            pil.thumbnail((COVER_W, COVER_H), Image.LANCZOS)
            photo = ImageTk.PhotoImage(pil)
            self._page_img_refs.append(photo)

            display_w_px = photo.width()
            display_h_px = photo.height()

            dh_design = _px_to_design(display_h_px)
            cover_y = CARD_Y + (dh_design // 2)  # ✅ bottom Y so center aligns to CARD_Y

            cover_lbl = tk.Label(self, image=photo, bg=THEME_COLOR2, bd=0)
            self.place_design(cover_lbl, COVER_X, cover_y, anchor="s")
            self.active_widgets.append(cover_lbl)
            self._book_detail_cover_widget = cover_lbl
            self._book_detail_cover_anchor = "s"

        else:
            # placeholder has known design height COVER_H, so it's easy
            dh_design = COVER_H
            cover_y = CARD_Y + (dh_design // 2)  # ✅ bottom Y so center aligns to CARD_Y

            ph = tk.Canvas(self, width=COVER_W, height=COVER_H, bg=SHARED_BLANKCOVER_BG_COLOR, highlightthickness=0)
            ph.create_text(
                COVER_W // 2,
                COVER_H // 2,
                text="No Cover",
                fill=SHARED_BLANKCOVER_TEXT_COLOR,
                font=(SHARED_FONT_CUSTOM, 16),
            )
            self.place_design(ph, COVER_X, cover_y, anchor="s")
            self.active_widgets.append(ph)
            self._book_detail_cover_widget = ph
            self._book_detail_cover_anchor = "s"

        # Store cover display size in DESIGN units (used by + button placement)
        dw_design = _px_to_design(display_w_px) if cover_path and cover_path.exists() else COVER_W
        dh_design = _px_to_design(display_h_px) if cover_path and cover_path.exists() else COVER_H
        self._book_detail_cover_display_w = dw_design
        self._book_detail_cover_display_h = dh_design


        plus_frame = tk.Frame(self, width=PLUS_W, height=PLUS_H, bg=SHARED_PLUSBTN_BG_COLOR, highlightthickness=0, bd=0)
        plus_frame.pack_propagate(False)

        self.place_design(plus_frame, PLUS_X, PLUS_Y, anchor="nw")
        self.active_widgets.append(plus_frame)
        self._book_detail_plus_frame = plus_frame
        self._book_detail_plus_anchor = "nw"

        plus_x_design = PLUS_X
        plus_y_design = PLUS_Y

        plus_btn = tk.Button(
            plus_frame,
            text="+",
            command=lambda b=book, pb=None: None,
            bg=BOOKDETAIL_TAGEDIT_SYMBOL_ONCLICK_COLOR,
            fg=BOOKDETAIL_TAGEDIT_SYMBOL_COLOR,
            activebackground=BOOKDETAIL_TAGHOLDER_SUBTEXT_COLOR,
            activeforeground=BOOKDETAIL_TAGEDIT_SYMBOL_ONCLICK_COLOR,
            bd=0,
            highlightthickness=0,
            relief="flat",
            takefocus=False,
            font=(BODY_FONT, S(16), "bold"),
        )
        plus_btn.pack(fill="both", expand=True)
        self.active_widgets.append(plus_btn)
        toggle_cmd = lambda b=book, pb=plus_btn, px=plus_x_design, py=plus_y_design: self._toggle_tags_editor(
            book=b, plus_btn=pb, design_x=px, design_y=py, S=S, BODY_FONT=BODY_FONT
        )
        plus_btn._toggle_cmd = toggle_cmd  # type: ignore[attr-defined]
        plus_btn.config(command=toggle_cmd)

        # ---------- info card ----------
        card = tk.Frame(self, bg=THEME_COLOR2, width=CARD_W, height=CARD_H)
        card.pack_propagate(False)
        self.place_design(card, CARD_X, CARD_Y, anchor="center")
        self.active_widgets.append(card)
        self._book_detail_card = card
        self._book_detail_card_anchor = "center"

        # --- title (wraps, so height is dynamic) ---
        if not getattr(self, "_book_edit_mode", False):
            title_lbl = tk.Label(
                card, text=title,
                bg=BOOKDETAIL_CARD_BG_COLOR, fg=BOOKDETAIL_CARD_TEXT_COLOR,
                font=(BODY_FONT, T(28), "bold"),
                wraplength=CARD_W - 2 * pad_x,
                anchor="w", justify="left"
            )
            title_lbl.place(x=pad_x, y=pad_y, anchor="nw")
            self._book_detail_title_lbl = title_lbl

            # Force geometry calc so winfo_height is correct
            card.update_idletasks()
            title_h = max(title_lbl.winfo_height(), T(42))
        else:
            # In-place editable title at the exact same position
            title_var = tk.StringVar(value=title)
            self._book_edit_vars["title"] = title_var

            title_entry = tk.Entry(
                card,
                textvariable=title_var,
                font=(BODY_FONT, S(22), "bold"),
                bd=0,
                bg=SHARED_ENTRY2_BG_COLOR,
                fg=SHARED_ENTRY2_TEXT_COLOR,
                highlightthickness=1,
                relief="flat",
                insertbackground=SHARED_ENTRY2_CURSOR_COLOR,
                insertwidth=2,  # Cursor width
            )
            title_entry.place(
                x=pad_x,
                y=pad_y,
                anchor="nw",
                width=CARD_W - 2 * pad_x,
                height=S(42),
            )
            self.active_widgets.append(title_entry)

            card.update_idletasks()
            title_h = S(42)
        gap_after_title = S(10)

        # --- author (placed under the real title height) ---
        author_y = pad_y + title_h + gap_after_title
        if not getattr(self, "_book_edit_mode", False):
            author_lbl = tk.Label(
                card, text=author,
                bg=BOOKDETAIL_CARD_BG_COLOR, fg=BOOKDETAIL_CARD_TEXT_COLOR,
                font=(BODY_FONT, T(22), "italic"),
                anchor="w", justify="left"
            )
            author_lbl.place(x=pad_x, y=author_y, anchor="nw")
            card.update_idletasks()
            author_h = max(author_lbl.winfo_height(), S(28))
        else:
            author_var = tk.StringVar(value=author)
            self._book_edit_vars["author"] = author_var

            author_entry = tk.Entry(
                card,
                textvariable=author_var,
                font=(BODY_FONT, T(18)),
                bg=SHARED_ENTRY2_BG_COLOR,
                fg=SHARED_ENTRY2_TEXT_COLOR,
                bd=0,
                highlightthickness=1,
                relief="flat",
                insertbackground=SHARED_ENTRY2_CURSOR_COLOR,  # Blinking cursor color
                insertwidth=2,  # Cursor width
            )
            author_entry.place(
                x=pad_x,
                y=author_y,
                anchor="nw",
                width=CARD_W - 2 * pad_x,
                height=S(32),
            )
            self.active_widgets.append(author_entry)
            card.update_idletasks()
            author_h = S(32)
        gap_after_author = S(14)

        # --- genre dropdown (only in edit mode, placed under author) ---
        genre_y = pad_y + title_h + gap_after_title + author_h + gap_after_author
        genre_h = 0
        if getattr(self, "_book_edit_mode", False):
            # Build genre choices from library data
            all_genres = set()
            try:
                all_genres.update(self.data.FICTION_GENRES)
                all_genres.update(self.data.NONFICTION_GENRES)
                # Add user-defined genres
                if hasattr(self.data, "user_genres"):
                    all_genres.update(self.data.user_genres)
                # Add genres from catalog
                for b in self.catalog:
                    g = (b.get("genre") or "").strip()
                    if g:
                        all_genres.add(g)
            except Exception:
                pass

            genre_choices = sorted(all_genres, key=str.lower)
            genre_choices.append("Add new genre…")

            genre_var = tk.StringVar(value=genre)
            self._book_edit_vars["genre"] = genre_var

            genre_label = tk.Label(
                card,
                text="Genre:",
                bg=BOOKEDIT_DESC_BG_COLOR,
                fg=BOOKEDIT_DESC_TEXT_COLOR,
                font=(BODY_FONT, S(14)),
                anchor="w",
            )
            genre_label.place(x=pad_x, y=genre_y, anchor="nw")
            self.active_widgets.append(genre_label)

            genre_combo = ttk.Combobox(
                card,
                textvariable=genre_var,
                values=genre_choices,
                state="readonly",
                font=(BODY_FONT, S(14)),
                width=25,
            )
            genre_combo.place(
                x=pad_x + S(60),
                y=genre_y,
                anchor="nw",
            )
            self.active_widgets.append(genre_combo)

            # Event handler for "Add new genre…" selection
            def _on_genre_select(event=None):
                selected = genre_var.get()
                if selected == "Add new genre…":
                    # Show popup to enter new genre
                    new_genre = simpledialog.askstring(
                        "Add New Genre",
                        "Enter the name for the new genre:",
                        parent=self
                    )
                    if new_genre and new_genre.strip():
                        new_genre = new_genre.strip().title()
                        # Save to user genres immediately
                        try:
                            self.data.add_user_genre(new_genre)
                        except Exception as e:
                            messagebox.showerror("Error", f"Could not save genre: {e}")
                            genre_var.set(genre)  # Reset to original
                            return

                        # Update the dropdown with the new genre
                        updated_choices = sorted(
                            set(genre_choices[:-1]) | {new_genre},
                            key=str.lower
                        )
                        updated_choices.append("Add new genre…")
                        genre_combo["values"] = updated_choices

                        # Set the new genre as selected
                        genre_var.set(new_genre)
                    else:
                        # User cancelled or entered empty - reset to original genre
                        genre_var.set(genre)

            genre_combo.bind("<<ComboboxSelected>>", _on_genre_select)

            card.update_idletasks()
            genre_h = S(36)
            gap_after_genre = S(10)
        else:
            gap_after_genre = 0

        # --- description box (placed under genre if in edit mode, else under author) ---
        desc_y = genre_y + genre_h + gap_after_genre if getattr(self, "_book_edit_mode", False) else (pad_y + title_h + gap_after_title + author_h + gap_after_author)
        desc_h = max(S(80), CARD_H - desc_y - S(14))  # bottom padding + min height

        desc_frame = tk.Frame(card, bg=THEME_COLOR2)
        desc_frame.place(
            x=pad_x, y=desc_y, anchor="nw",
            width=CARD_W - 2 * pad_x,
            height=desc_h
        )
        self._book_detail_desc_frame = desc_frame
        self._book_detail_desc_pad_x = pad_x

        scroll = tk.Scrollbar(desc_frame)
        scroll.pack(side="right", fill="y")

        desc_text = tk.Text(
            desc_frame,
            wrap="word",
            bg=BOOKDETAIL_CARD_BG_COLOR,
            fg=BOOKDETAIL_CARD_TEXT_COLOR,
            font=(BODY_FONT, T(18 if fs else 16)),
            bd=0,
            highlightthickness=(1 if getattr(self, "_book_edit_mode", False) else 0),
            highlightbackground=("black" if getattr(self, "_book_edit_mode", False) else BOOKDETAIL_CARD_BG_COLOR),
            yscrollcommand=scroll.set,
            spacing1=S(2), spacing2=S(2), spacing3=S(6),
            insertbackground=SHARED_ENTRY_CURSOR_COLOR,
            insertwidth=2,  # Cursor width
        )
        desc_text.pack(side="left", fill="both", expand=True)
        self._book_detail_desc_text = desc_text
        scroll.config(command=desc_text.yview)

        desc_text.insert("1.0", desc)
        if getattr(self, "_book_edit_mode", False):
            # editable in place
            desc_text.config(state="normal")
            self._book_edit_vars["description_widget"] = desc_text
        else:
            desc_text.config(state="disabled")

        # --- Save/Cancel buttons (OUTSIDE the card, below it) ---
        if getattr(self, "_book_edit_mode", False):
            BTN_W = S(150)
            BTN_H = S(40)
            GAP = S(18)  # gap below the card
            BETWEEN = S(14)  # spacing between buttons

            # card geometry in DESIGN units
            card_top = CARD_Y - (CARD_H // 2)
            card_bottom = card_top + CARD_H

            # align buttons to the right edge of the card (outside)
            right_edge = (CARD_X + (CARD_W // 2)) - pad_x
            btn_y = card_bottom + GAP

            cancel_x = right_edge - (BTN_W * 2) - BETWEEN
            save_x = right_edge - BTN_W

            cancel_btn = tk.Button(
                self,
                text="Cancel",
                command=self._side_cancel_book_edit,
                bg=SHARED_BUTTON1_BG_COLOR,
                fg=SHARED_BUTTON1_TEXT_COLOR,
                activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
                activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
                bd=0,
                highlightthickness=0,
                font=(SHARED_FONT_BUTTON, T(20)),
                cursor="hand2",
            )
            self.place_design(cancel_btn, cancel_x, btn_y, anchor="nw")
            cancel_btn.configure(width=1)  # ignore text-width sizing
            cancel_btn.place_configure(width=BTN_W, height=BTN_H)
            self.active_widgets.append(cancel_btn)

            save_btn = tk.Button(
                self,
                text="Save",
                command=self._side_save_book_edit,
                bg=SHARED_BUTTON1_BG_COLOR,
                fg=SHARED_BUTTON1_TEXT_COLOR,
                activebackground=SHARED_BUTTON1_BG_ONCLICK_COLOR,
                activeforeground=SHARED_BUTTON1_TEXT_ONCLICK_COLOR,
                bd=0,
                highlightthickness=0,
                font=(SHARED_FONT_BUTTON, T(20)),
                cursor="hand2",
            )
            self.place_design(save_btn, save_x, btn_y, anchor="nw")
            save_btn.configure(width=1)
            save_btn.place_configure(width=BTN_W, height=BTN_H)
            self.active_widgets.append(save_btn)

            # store refs for relayout
            self._book_detail_save_btn = save_btn
            self._book_detail_cancel_btn = cancel_btn
            self._book_detail_btn_anchor = "nw"
            self.active_widgets.append(cancel_btn)
            self.active_widgets.append(save_btn)
        self._book_detail_last_fs = bool(self._is_fullscreen_like())
        self.mount_left_nav()
    def _book_detail_relayout(self):
        """Recompute fullscreen-like layout and move/resize existing book detail widgets."""
        if getattr(self, "current_page", "") != "book_detail":
            return

        card = getattr(self, "_book_detail_card", None)
        cover = getattr(self, "_book_detail_cover_widget", None)
        plus_frame = getattr(self, "_book_detail_plus_frame", None)
        tags_frame = getattr(self, "_book_detail_tags_frame", None)
        isbn_lbl = getattr(self, "_book_detail_isbn_lbl", None)

        # If page isn’t fully built yet, bail
        if not (card and card.winfo_exists() and cover and cover.winfo_exists()):
            return

        fs = bool(self._is_fullscreen_like())

        # --- recompute scale (must match show_book_detail) ---
        self.update_idletasks()
        win_w = max(self.winfo_width(), 1)
        scale = max(0.85, min(1.45, win_w / 1280))

        def S(px: int) -> int:
            return max(10, int(round(px * scale)))

        # --- base geometry (must match show_book_detail) ---
        COVER_X = 330
        ISBN_Y = 620
        COVER_W, COVER_H = 260, 380
        COVER_GAP = 25

        CARD_X, CARD_Y = 840, 460
        CARD_W, CARD_H = 640, 320
        TAGS_Y_DROP = 0

        if fs:
            ISBN_Y = 620 + S(30)
            COVER_X = 210
            CARD_X = 920
            CARD_W = 820
            CARD_H = 420
            GENRE_GAP = S(10)
            TAGS_Y_DROP = S(18)

        # --- cover position depends on ISBN_Y ---
        cover_y = ISBN_Y - COVER_GAP

        # 1) update card size + position FIRST
        try:
            card.configure(width=CARD_W, height=CARD_H)
        except Exception:
            pass
        self._update_design_placement_record(
            card, CARD_X, CARD_Y,
            anchor=getattr(self, "_book_detail_card_anchor", "center")
        )

        # 2) update ISBN position (AFTER COVER_X is finalized)
        if isbn_lbl and isbn_lbl.winfo_exists():
            self._update_design_placement_record(
                isbn_lbl, COVER_X, ISBN_Y,
                anchor=getattr(self, "_book_detail_isbn_anchor", "s")
            )

        # 3) update cover position (AFTER COVER_X is finalized)
        self._update_design_placement_record(
            cover, COVER_X, cover_y,
            anchor=getattr(self, "_book_detail_cover_anchor", "s")
        )

        # 4) update plus_frame position (to the LEFT of tags frame)
        if plus_frame and plus_frame.winfo_exists():
            pad_x = 20
            card_left = CARD_X - (CARD_W // 2)
            TAGS_X = card_left + pad_x
            TAGS_Y = 650 + (S(22) if fs else 0) + TAGS_Y_DROP

            PLUS_W = 34
            PLUS_GAP = 10
            PLUS_X = TAGS_X - PLUS_W - PLUS_GAP
            PLUS_Y = TAGS_Y

            self._update_design_placement_record(
                plus_frame,
                PLUS_X,
                PLUS_Y,
                anchor=getattr(self, "_book_detail_plus_anchor", "nw"),
            )

        # 5) update genre canvas pinned coords
        # keep layout dict fresh for sync_genre_position()
        self._book_detail_layout = {
            "CARD_X": CARD_X, "CARD_Y": CARD_Y,
            "CARD_W": CARD_W, "CARD_H": CARD_H,
            "pad_x": 20,
            "GENRE_GAP": S(10),
        }
        # update genre font size with new scale so metrics match
        genre_font = getattr(self, "_book_detail_genre_font", None)
        if genre_font:
            try:
                genre_font.configure(size=S(42))
            except Exception:
                pass

        # 6) update tags frame placement
        if tags_frame and tags_frame.winfo_exists():
            pad_x = 20
            card_left = CARD_X - (CARD_W // 2)
            TAGS_X = card_left + pad_x
            TAGS_Y = 650 + (S(22) if fs else 0) + TAGS_Y_DROP

            self._update_design_placement_record(
                tags_frame, TAGS_X, TAGS_Y,
                anchor=getattr(self, "_book_detail_tags_frame_anchor", "nw")
            )
            # keep your stored coords consistent (even though frame is used)
            self._book_detail_tags = {"x": TAGS_X, "y": TAGS_Y}

        # 7) NOW resize the description frame AFTER the card is resized
        desc_frame = getattr(self, "_book_detail_desc_frame", None)
        if desc_frame and desc_frame.winfo_exists():
            pad_x = int(getattr(self, "_book_detail_desc_pad_x", 20))
            new_w = max(120, CARD_W - 2 * pad_x)

            info = desc_frame.place_info()
            y = int(float(info.get("y", 0)))
            new_h = max(80, CARD_H - y - S(14))

            desc_frame.place_configure(width=new_w, height=new_h)
            desc_frame.update_idletasks()

        # Optional: if you decide to store title_lbl, update wraplength here too
        title_lbl = getattr(self, "_book_detail_title_lbl", None)
        if title_lbl and title_lbl.winfo_exists():
            pad_x = 20
            title_lbl.configure(wraplength=max(120, CARD_W - 2 * pad_x))
        # after layout + font updates, move genre into correct spot
        self._book_detail_sync_genre_position()
        # 8) update Save/Cancel buttons (outside the card)
        save_btn = getattr(self, "_book_detail_save_btn", None)
        cancel_btn = getattr(self, "_book_detail_cancel_btn", None)

        if getattr(self, "_book_edit_mode", False) and save_btn and cancel_btn:
            if save_btn.winfo_exists() and cancel_btn.winfo_exists():
                BTN_W = S(150)
                BTN_H = S(40)
                GAP = S(18)
                BETWEEN = S(14)

                pad_x = 20
                card_top = CARD_Y - (CARD_H // 2)
                card_bottom = card_top + CARD_H
                right_edge = (CARD_X + (CARD_W // 2)) - pad_x
                btn_y = card_bottom + GAP

                cancel_x = right_edge - (BTN_W * 2) - BETWEEN
                save_x = right_edge - BTN_W

                self._update_design_placement_record(
                    cancel_btn, cancel_x, btn_y,
                    anchor=getattr(self, "_book_detail_btn_anchor", "nw")
                )
                cancel_btn.place_configure(width=BTN_W, height=BTN_H)

                self._update_design_placement_record(
                    save_btn, save_x, btn_y,
                    anchor=getattr(self, "_book_detail_btn_anchor", "nw")
                )
                save_btn.place_configure(width=BTN_W, height=BTN_H)

    # ---------- LOGIC HELPERS ----------
    def _unescape_entities(self, s: str) -> str:
        s = (s or "").strip()
        for _ in range(2):
            new = html.unescape(s)
            if new == s:
                break
            s = new
        return s
    def _get_author_parts(self, row: dict) -> tuple[str, str, str]:
        """
        Extract author parts from a book dict.
        Returns: (first_name, last_name, creators)
        """
        first = (row.get("first_name") or "").strip()
        last = (row.get("last_name") or "").strip()
        creators = (row.get("creators") or "").strip()
        return first, last, creators
    def _format_author_display(self, row: dict, format_style: str = "last_first") -> str:
        """
        Format author for display.
        format_style: "last_first" -> "Doe, John"
                      "first_last" -> "John Doe"
        """
        first, last, creators = self._get_author_parts(row)
        
        if last or first:
            if format_style == "last_first":
                return f"{last}, {first}".strip(", ").strip()
            else:
                return f"{first} {last}".strip()
        elif creators:
            return creators.strip()
        return "Unknown author"
    def _get_author_sort_key(self, row: dict) -> tuple[str, str, str]:
        """Get sort key tuple for author sorting: (last, first, title)"""
        first, last, creators = self._get_author_parts(row)
        title = self._unescape_entities(row.get("title") or "Untitled")
        
        if last or first:
            sort_last = last.lower() or "zzz"
            sort_first = first.lower()
        elif creators:
            parts = creators.split()
            sort_last = parts[-1].lower() if parts else "zzz"
            sort_first = " ".join(parts[:-1]).lower() if len(parts) >= 2 else ""
        else:
            sort_last = "zzz"
            sort_first = ""
        
        title_sort = title.lower()
        return (sort_last, sort_first, title_sort)
    def _author_display_and_sort_key(self, row: dict):
        """Get author display string and sort key tuple."""
        display = self._format_author_display(row, "last_first")
        sort_key = self._get_author_sort_key(row)
        return display, sort_key
    def _get_display_fields(self, row: dict) -> tuple[str, str, str]:
        title = self._unescape_entities(row.get("title") or "Untitled")
        author = self._format_author_display(row, "last_first")

        year = (row.get("_year") or "").strip()
        if not year:
            publish_date = (
                row.get("publish_date")
                or row.get("date_published")
                or ""
            ).strip()
            if publish_date:
                year = publish_date.split("-")[0]

        return author, title, year
    def _filter_books_by_genre(self, genre_name: str) -> list[dict]:
        g = (genre_name or "").strip().lower()
        out = []
        for b in self.catalog:
            bg = (b.get("genre") or "").strip().lower()
            if bg == g:
                out.append(b)
        return out
    def perform_search(self, query: str):
        # Reset book edit mode when navigating away via search
        self._book_edit_mode = False
        
        query = (query or "").strip().lower()

        if not query:
            results = self.catalog[:]
        else:
            tokens = query.split()
            results: list[dict] = []

            for row in self.catalog:
                search_text = row.get("search_text")
                if not search_text:
                    title = (row.get("title") or "")
                    creators = (row.get("creators") or "")
                    first_name = (row.get("first_name") or "")
                    last_name = (row.get("last_name") or "")
                    date_published = (row.get("date_published") or "")
                    search_text = " ".join(
                        [title, creators, first_name, last_name, date_published]
                    ).lower()

                if all(tok in search_text for tok in tokens):
                    publish_date = (row.get("publish_date") or "").strip()
                    year = publish_date.split("-")[0] if publish_date else ""
                    row["_year"] = year
                    results.append(row)

        self.last_search_results = results
        self.last_search_query = query

        self.show_search_results(results, original_query=query)
    def open_random_book(self):
        if not self.catalog:
            messagebox.showinfo("Random Book", "No books in the library yet.")
            return
        book = random.choice(self.catalog)
        self.show_book_detail(book)


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
