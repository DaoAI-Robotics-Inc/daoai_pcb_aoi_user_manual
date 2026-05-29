"""Capture English-UI screenshots of the AOI web client.

The FE serves English UI strings already. Each capture is saved as
``<name>.en.png`` next to its zh_CN counterpart so Sphinx's default
``figure_language_filename = '{root}.{language}{ext}'`` picks it up for the
en build and falls back to the original for the zh_CN build.

Image paths come from ``image_map.json`` (rebuilt by ``build_image_map.py``).

SSE keeps the network busy, so we never wait for ``networkidle`` — we use
``domcontentloaded`` plus fixed waits.

Usage::

    python capture_en.py [batch]

``batch`` is one of: ``login``, ``home``, ``settings``, ``teach``, ``inspect``,
``worklist``, ``models``, ``all``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_ROOT = REPO_ROOT / "daoai_pcb_aoi_user_manual" / "docs" / "source"
IMAGE_MAP_FILE = Path(__file__).resolve().parent / "image_map.json"

FE_URL = "http://localhost:3005"
ADMIN_USER = "admin"
ADMIN_PASS = "2446bd05"

# Skip these — captured externally or covered by another image.
SKIP = {
    # Win32 / OS-native — user agreed to leave the Chinese.
    "instance_manager.png",
    "nv_power.png",
    "ctrlpanel_power.png",
    "edge_hardware_acc.png",
    "edge_hardware_acc2.png",
    "edge_hardware_acc3.png",
    "aoi_pcb_blob_liner.png",
    "archive_file_in_target_volume.png",
    # Placeholder, no zh image either.
    "variation_overview.png",
}

with IMAGE_MAP_FILE.open(encoding="utf-8") as f:
    IMAGE_MAP: dict[str, list[str]] = json.load(f)


def en_targets(basename: str) -> list[Path]:
    """Return all .en.png paths for an image basename (a few are referenced
    from more than one location).
    """
    if basename in SKIP:
        return []
    paths = IMAGE_MAP.get(basename, [])
    out: list[Path] = []
    for rel in paths:
        p = DOC_ROOT / rel
        out.append(p.with_name(p.stem + ".en" + p.suffix))
    return out


def shot(page: Page, basename: str, *, locator=None, clip: dict | None = None,
         full_page: bool = False) -> bool:
    targets = en_targets(basename)
    if not targets:
        print(f"  - {basename}: skipped (in SKIP or not referenced)")
        return False
    try:
        # Take the screenshot once into the first target, then copy to the rest.
        first = targets[0]
        first.parent.mkdir(parents=True, exist_ok=True)
        if locator is not None:
            locator.screenshot(path=str(first))
        elif clip is not None:
            page.screenshot(path=str(first), clip=clip)
        elif full_page:
            page.screenshot(path=str(first), full_page=True)
        else:
            page.screenshot(path=str(first))
        for extra in targets[1:]:
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_bytes(first.read_bytes())
        for t in targets:
            print(f"  ✓ {t.relative_to(DOC_ROOT)}")
        return True
    except Exception as e:
        print(f"  ✗ {basename}: {e}")
        return False


def login(page: Page) -> None:
    page.goto(f"{FE_URL}/login", wait_until="domcontentloaded")
    page.wait_for_timeout(1_500)
    page.locator("input[placeholder='Username']").fill(ADMIN_USER)
    page.locator("input[type='password']").fill(ADMIN_PASS)
    page.locator("button:has-text('Login')").first.click()
    page.wait_for_url("**/home", timeout=15_000)
    page.wait_for_timeout(3_000)


def goto(page: Page, path: str, wait_ms: int = 2_500) -> None:
    page.goto(f"{FE_URL}{path}", wait_until="domcontentloaded")
    page.wait_for_timeout(wait_ms)


def click_text(page: Page, text_regex: str, wait_after: int = 800,
               timeout: int = 4_000) -> bool:
    """Click the first element matching a /regex/ text locator."""
    try:
        page.locator(f"text=/{text_regex}/").first.click(timeout=timeout)
        page.wait_for_timeout(wait_after)
        return True
    except Exception as e:
        print(f"  ! click '{text_regex}' failed: {type(e).__name__}: {e!s:.80}")
        return False


# ---------------------------------------------------------------------------
# Batches
# ---------------------------------------------------------------------------

def capture_login(page: Page) -> None:
    print("[login]")
    # Navigate to the FE first; about:blank denies localStorage access.
    page.goto(f"{FE_URL}/login", wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    try:
        page.evaluate("localStorage.clear()")
    except Exception:
        pass
    page.context.clear_cookies()
    goto(page, "/login", wait_ms=1_500)
    shot(page, "login.png")

    # Change Host Address dialog
    page.locator("button:has-text('Change Host Address')").first.click()
    page.wait_for_timeout(700)
    shot(page, "host_addr.png")
    shot(page, "change_host.png")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)


def capture_home(page: Page) -> None:
    print("[home]")
    goto(page, "/home")
    shot(page, "home.png")
    # Disk-usage widget — crop the top-right corner including the disk %.
    shot(page, "disk_usage_widget.png",
         clip={"x": 1190, "y": 8, "width": 380, "height": 32})


def capture_settings(page: Page) -> None:
    print("[settings]")
    goto(page, "/settings")
    shot(page, "settings.png")

    # Make sure the System Settings group is expanded.
    try:
        page.locator("text=/^System Settings$/").first.click(timeout=3_000)
        page.wait_for_timeout(400)
    except Exception:
        pass

    # Actual sidebar labels (from the live UI): Language, Host, System Config,
    # Capture Agent, Model Updater, Teach Default Params, Error Type
    # Translation, Tags, Calibration, About, Log.
    if click_text(page, "^System Config$", wait_after=1_500):
        shot(page, "system_setting.png")

    if click_text(page, "^Language$"):
        shot(page, "change_language.png")

    if click_text(page, "^Calibration$"):
        shot(page, "infield_calibration.png")

    if click_text(page, "^Log$"):
        shot(page, "system_log.PNG")

    if click_text(page, "^Error Type Translation$"):
        shot(page, "error_type_translation.png")

    if click_text(page, "^Teach Default Params$"):
        shot(page, "default_program_params.PNG")

    if click_text(page, "^Capture Agent$", wait_after=1_000):
        # The original 2d_camera_settings is a tight crop of the light/sensor
        # section. Capture the whole sub-page; a follow-up crop pass can tighten
        # this if needed.
        shot(page, "2d_camera_settings.png")

    # Team (admin only)
    if click_text(page, "^Team$"):
        shot(page, "manage_user.png")
        # manage_user2 is a different view of the same screen — sometimes a
        # "Add user" modal. Try clicking add to capture, then close.
        try:
            page.locator("button:has-text('Add')").first.click(timeout=3_000)
            page.wait_for_timeout(800)
            shot(page, "manage_user2.png")
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)
        except Exception:
            # No add modal; reuse the manage_user shot.
            shot(page, "manage_user2.png")

    # Manage Models — top-level sidebar entry
    if click_text(page, "^Manage Models$", wait_after=1_500):
        shot(page, "manage_models.png")


def capture_worklist(page: Page) -> None:
    print("[worklist]")
    goto(page, "/worklist", wait_ms=3_000)
    shot(page, "worklist.png")

    if click_text(page, "^Inspection Result$", wait_after=1_500) or \
            click_text(page, "^Inspection Results$", wait_after=1_500):
        shot(page, "worklist1.png")

    # worklist2.png is the Review-detail page reached from View. Try to click
    # the first View button.
    try:
        page.locator("button:has-text('View')").first.click(timeout=4_000)
        page.wait_for_url("**/inspection/review**", timeout=10_000)
        page.wait_for_timeout(4_000)
        shot(page, "worklist2.png")
        shot(page, "review_page_overview.png")
    except Exception as e:
        print(f"  ! worklist2/review_page_overview: {e}")


def capture_models(page: Page) -> None:
    print("[models]")
    goto(page, "/models")
    shot(page, "models_page.png")
    shot(page, "models_dataset_page.png")
    # Training view
    if click_text(page, "^Training$", wait_after=1_500) or \
            click_text(page, "^Train$", wait_after=1_500):
        shot(page, "models_train_page.png")


def capture_teach(page: Page) -> None:
    print("[teach]")
    goto(page, "/home", wait_ms=3_000)
    # Find Edit coords for the fully-configured "speed test-copy-copy" row by
    # exact name match. Locator filter is too fuzzy (matches "speed test-copy"
    # too); JS eval keeps the equality test strict.
    coords = page.evaluate("""() => {
        for (const tr of document.querySelectorAll('tr.ant-table-row')) {
            const name = tr.querySelectorAll('td')[1]?.textContent.trim();
            if (name === 'speed test-copy-copy') {
                const edit = Array.from(tr.querySelectorAll('span.cursor-pointer'))
                    .find(s => s.textContent.trim() === 'Edit');
                const r = edit?.getBoundingClientRect();
                return r ? {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)} : null;
            }
        }
        return null;
    }""")
    if not coords:
        print("  ! 'speed test-copy-copy' row not found on home page")
        return
    page.mouse.click(coords["x"], coords["y"])
    page.wait_for_url("**/teach**", timeout=15_000)
    page.wait_for_timeout(7_000)

    # The fully-configured product lands on the Template Editor (Component
    # view). Capture Component-side shots first, then navigate to Recipe.

    # ---- Component view (default landing) ----
    shot(page, "template_editor.png")
    shot(page, "component_list.png")
    shot(page, "component_list_view.png")

    # ---- Top horizontal tabs ----
    def wait_for_no_overlay(timeout_ms: int = 10_000) -> None:
        """Spin until no fixed-overlay blocker covers the page."""
        page.wait_for_function(
            """() => !document.querySelector('.fixed.inset-0.bg-black\\\\/50')""",
            timeout=timeout_ms,
        )

    def click_top_tab(label_substring: str, wait_after: int = 2_500) -> bool:
        """Click a top-tab by partial label text (handles labels with /)."""
        try:
            wait_for_no_overlay()
        except Exception:
            pass
        try:
            page.locator(
                f".ant-tabs-tab-btn", has_text=label_substring
            ).first.click(timeout=4_000)
            page.wait_for_timeout(wait_after)
            return True
        except Exception as e:
            print(f"  ! top-tab '{label_substring}' failed: {type(e).__name__}")
            return False

    # Marker/ Align PCB (note the singular and the space after /)
    if click_top_tab("Marker/"):
        shot(page, "mark_align_pcb_overview.png")
        shot(page, "mark_alignment.png")
        shot(page, "mark_point_example.png")

    # PCB Array
    if click_top_tab("PCB Array"):
        shot(page, "pcb_array_1.png")

    # Whole Board Inspection
    if click_top_tab("Whole Board Inspection"):
        shot(page, "whole_board_inspection_overview.png")

    # Collinearity Inspection
    if click_top_tab("Collinearity Inspection"):
        shot(page, "collinearity.png")

    # Back to Template Editor for the Recipe-rail shots
    click_top_tab("Template Editor")

    # ---- Recipe rail ----
    # The left rail shows two vertical buttons: Recipe and Component. Click the
    # Recipe button. Wait for any loading overlay to dismiss first.
    try:
        wait_for_no_overlay(timeout_ms=15_000)
    except Exception:
        pass
    try:
        page.locator(
            "button.flex.flex-col:has(span:text-is('Recipe'))"
        ).first.click(timeout=5_000)
        page.wait_for_timeout(3_000)
    except Exception as e:
        print(f"  ! Recipe rail click failed: {type(e).__name__}")
        return

    # Now on the Recipe view; capture sub-tabs.
    shot(page, "recipe_pcb_detail.png")
    shot(page, "recipe_tabs.png")

    if click_text(page, "^Conveyor Setup$", wait_after=1_500):
        shot(page, "recipe_conveyor_setup.png")

    if click_text(page, "^Inspection Settings$", wait_after=1_500):
        shot(page, "recipe_inspection_settings.png")


def capture_review_from_worklist(page: Page) -> None:
    """Open a historical inspection from the Worklist and capture the Review
    page (review_page_overview, worklist2, inspect_review_page).
    """
    print("[review]")
    goto(page, "/worklist", wait_ms=2_500)
    # Switch to Inspection Result and widen the range to This Year so there's
    # something to click View on.
    if not click_text(page, "^Inspection Result$", wait_after=1_500):
        return
    if click_text(page, "^This Year$", wait_after=2_500):
        pass
    # Click first View link (styled span, like the home Edit).
    try:
        view = page.locator("span.cursor-pointer", has_text="View").first
        view.click(timeout=5_000)
    except Exception as e:
        print(f"  ! View click: {e}")
        return
    page.wait_for_url("**/inspection/review**", timeout=15_000)
    page.wait_for_timeout(6_000)
    shot(page, "review_page_overview.png")
    shot(page, "worklist2.png")
    shot(page, "inspect_review_page.png")


def capture_extras(page: Page) -> None:
    """Extra UI artifacts: New Inspection Task modal, template editor search."""
    print("[extras]")
    # ---- New Inspection Task modal (start_inspection.png) ----
    goto(page, "/home", wait_ms=3_000)
    try:
        # Click the "New Inspection Task" action card.
        page.locator("text=/New Inspection Task/").first.click(timeout=5_000)
        page.wait_for_timeout(2_500)
        shot(page, "start_inspection.png")
        # Close.
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(800)
    except Exception as e:
        print(f"  ! start_inspection: {e}")

    # ---- Template Editor search (search.png) ----
    goto(page, "/home", wait_ms=2_500)
    coords = page.evaluate("""() => {
        for (const tr of document.querySelectorAll('tr.ant-table-row')) {
            const n = tr.querySelectorAll('td')[1]?.textContent.trim();
            if (n === 'speed test-copy-copy') {
                const e = Array.from(tr.querySelectorAll('span.cursor-pointer')).find(s => s.textContent.trim() === 'Edit');
                const r = e?.getBoundingClientRect();
                return r ? {x: Math.round(r.x+r.width/2), y: Math.round(r.y+r.height/2)} : null;
            }
        }
    }""")
    if not coords:
        return
    page.mouse.click(coords["x"], coords["y"])
    page.wait_for_url("**/teach**", timeout=15_000)
    page.wait_for_timeout(7_000)
    # The Template Editor lands by default. Find the search bar above the
    # component list.
    try:
        search_box = page.locator("input[placeholder*='Search'], input[placeholder*='search']").first
        # Crop the component-list panel (left side, ~300px wide).
        shot(page, "search.png",
             clip={"x": 100, "y": 60, "width": 350, "height": 600})
    except Exception as e:
        print(f"  ! search.png: {e}")

    # ---- Manual programming toolbar (manual_tools.png) ----
    # The right-side draw-toolbar appears in the Template Editor.
    try:
        # Toolbar is a vertical strip on the right edge of the canvas.
        shot(page, "manual_tools.png",
             clip={"x": 1535, "y": 60, "width": 60, "height": 540})
    except Exception as e:
        print(f"  ! manual_tools: {e}")


BATCHES: dict[str, Callable[[Page], None]] = {
    "login": capture_login,
    "home": capture_home,
    "settings": capture_settings,
    "teach": capture_teach,
    "worklist": capture_worklist,
    "models": capture_models,
    "extras": capture_extras,
    "review": capture_review_from_worklist,
}


def main() -> None:
    batch = sys.argv[1] if len(sys.argv) > 1 else "all"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1600, "height": 1000})
        page = ctx.new_page()

        if batch != "login":
            login(page)

        if batch == "all":
            for name in ("home", "settings", "teach", "worklist", "models"):
                try:
                    BATCHES[name](page)
                except Exception as e:
                    print(f"[!] batch {name} crashed: {e}")
            capture_login(page)
        else:
            BATCHES[batch](page)

        browser.close()


if __name__ == "__main__":
    main()
