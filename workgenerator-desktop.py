#!/usr/bin/env python3
"""
AI Work Generator Framework - Desktop GUI
A PyQt5-based interface for the work generator framework.

Usage: python3 workgenerator-desktop.py
       Or set USE_GUI=true and run ./workgenerator.sh
"""

import base64
import os
import subprocess
import sys
from collections import deque

from PyQt5 import QtCore, QtGui, QtWidgets

MAX_VISIBLE_MESSAGES = 200


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    import re
    return re.sub(r"\x1B\[[0-9;?]*[A-Za-z]", "", text)


class GlowFrame(QtWidgets.QFrame):
    """Frame with animated glow effect."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(28)
        self.effect.setOffset(0, 0)
        self.setGraphicsEffect(self.effect)
        self._hue = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._tick)

    def start_glow(self):
        if not self.timer.isActive():
            self.timer.start(120)

    def stop_glow(self, color=QtGui.QColor("#4ad7ff")):
        self.timer.stop()
        self.effect.setColor(color)

    def _tick(self):
        color = QtGui.QColor()
        color.setHsv(self._hue % 360, 180, 255, 210)
        self.effect.setColor(color)
        self._hue += 11


class MessageWidget(QtWidgets.QFrame):
    """Styled message widget for different content types."""

    STYLES = {
        "log": ("#f3f8ff", "rgba(255,255,255,0.06)", "#5f749d"),
        "phase": ("#ddfbff", "rgba(96,231,255,0.14)", "#6be8ff"),
        "assistant": ("#fff3ce", "rgba(255,209,102,0.12)", "#ffd166"),
        "user": ("#eef6ff", "rgba(106,123,255,0.34)", "#9dd7ff"),
        "plan": ("#ddffe8", "rgba(84,224,136,0.16)", "#88f2a8"),
        "error": ("#ffd5d8", "rgba(255,109,120,0.18)", "#ff7c86"),
        "system": ("#eef6ff", "rgba(255,255,255,0.05)", "#a1b5d9"),
    }

    def __init__(self, kind: str, text: str, highlighted: bool = False):
        super().__init__()
        fg, bg, accent = self.STYLES.get(kind, self.STYLES["log"])
        border = accent if highlighted else "rgba(255,255,255,0.08)"
        self.setStyleSheet(
            f"""
            QFrame {{
              background: {bg};
              border: 1px solid {border};
              border-radius: 18px;
            }}
            QLabel#meta {{
              color: {accent};
              font-size: 10px;
              font-weight: 700;
              letter-spacing: 0.18em;
            }}
            QLabel#body {{
              color: {fg};
              font-size: 13px;
            }}
            """
        )
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        meta = QtWidgets.QLabel(kind.upper())
        meta.setObjectName("meta")
        body = QtWidgets.QLabel(text)
        body.setObjectName("body")
        body.setWordWrap(True)
        body.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        layout.addWidget(meta)
        layout.addWidget(body)


class WorkGeneratorDesktop(QtWidgets.QMainWindow):
    """Main desktop application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Work Generator Framework")
        self.resize(1460, 940)
        self.setMinimumSize(1180, 760)

        self.messages = deque()
        self.backend = None
        self.pending_decision = None
        self.pending_improvement = False
        self.last_task = "Starting backend"
        self.auto_decision = os.getenv("WORKGENERATOR_DESKTOP_AUTODECISION")
        self.auto_improvement = os.getenv("WORKGENERATOR_DESKTOP_AUTOIMPROVEMENT", "")
        self.auto_quit = os.getenv("WORKGENERATOR_DESKTOP_AUTOQUIT", "false").lower() == "true"

        self._build_ui()
        self._apply_style()
        self._start_backend()

    def _build_ui(self):
        """Build the user interface."""
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        app_layout = QtWidgets.QHBoxLayout(central)
        app_layout.setContentsMargins(18, 18, 18, 18)
        app_layout.setSpacing(18)

        # Left panel
        left = QtWidgets.QFrame()
        left_layout = QtWidgets.QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)

        # Header
        header = QtWidgets.QFrame()
        header_layout = QtWidgets.QVBoxLayout(header)
        header_layout.setContentsMargins(24, 20, 24, 18)
        title = QtWidgets.QLabel("🚀 WORK GENERATOR")
        title.setObjectName("title")
        subtitle = QtWidgets.QLabel("AI-powered project idea generator and execution framework")
        subtitle.setObjectName("subtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        # HUD (Heads-Up Display)
        hud_layout = QtWidgets QHBoxLayout()
        hud_layout.setSpacing(10)
        status_pill, self.status_value = self._make_pill("Status", "Connecting")
        phase_pill, self.phase_value = self._make_pill("Phase", "Booting")
        backend_pill, self.backend_value = self._make_pill("Backend", "Starting")
        hud_layout.addWidget(status_pill)
        hud_layout.addWidget(phase_pill)
        hud_layout.addWidget(backend_pill)
        hud_layout.addStretch(1)
        header_layout.addLayout(hud_layout)

        # Spotlight (current task display)
        self.spotlight = GlowFrame()
        spotlight_layout = QtWidgets.QVBoxLayout(self.spotlight)
        spotlight_layout.setContentsMargins(20, 18, 20, 18)
        spotlight_tag = QtWidgets.QLabel("CURRENT TASK")
        spotlight_tag.setObjectName("spotlightTag")
        self.spotlight_phase = QtWidgets.QLabel("Booting")
        self.spotlight_phase.setObjectName("spotlightPhase")
        self.spotlight_task = QtWidgets.QLabel("Starting backend...")
        self.spotlight_task.setObjectName("spotlightTask")
        self.spotlight_task.setWordWrap(True)
        spotlight_layout.addWidget(spotlight_tag)
        spotlight_layout.addWidget(self.spotlight_phase)
        spotlight_layout.addWidget(self.spotlight_task)
        self.spotlight.start_glow()

        # Transcript (message log)
        self.transcript_list = QtWidgets.QListWidget()
        self.transcript_list.setSpacing(10)
        self.transcript_list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.transcript_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.transcript_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        left_layout.addWidget(header)
        left_layout.addWidget(self.spotlight)
        left_layout.addWidget(self.transcript_list, 1)

        # Right panel
        right = QtWidgets.QFrame()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(14)

        # Portfolio card
        self.portfolio_card = self._make_card("📊 Portfolio State")
        self.portfolio_text = QtWidgets.QLabel("Loading configuration...")
        self.portfolio_text.setWordWrap(True)
        self.portfolio_text.setObjectName("portfolioText")
        self.portfolio_card.layout().addWidget(self.portfolio_text)

        # Approval card
        self.approval_card = GlowFrame()
        approval_layout = QtWidgets.QVBoxLayout(self.approval_card)
        approval_layout.setContentsMargins(18, 18, 18, 18)
        approval_title = QtWidgets.QLabel("⚡ Decision Required")
        approval_title.setObjectName("cardTitle")
        self.approval_text = QtWidgets.QLabel("No decision pending right now.")
        self.approval_text.setWordWrap(True)
        self.approval_text.setObjectName("approvalText")
        approval_layout.addWidget(approval_title)
        approval_layout.addWidget(self.approval_text)

        # Decision buttons
        approval_buttons = QtWidgets.QGridLayout()
        approval_buttons.setSpacing(10)
        self.approve_btn = self._make_action_button("✓ Approve", "#88f2a8", "#0d2918")
        self.reject_btn = self._make_action_button("✗ Reject", "#ff7c86", "#2b0a0f")
        self.pass_btn = self._make_action_button("⏭ Pass", "#ffd166", "#2e2000")
        self.improve_btn = self._make_action_button("✎ Improve", "#87baff", "#091631")
        approval_buttons.addWidget(self.approve_btn, 0, 0)
        approval_buttons.addWidget(self.reject_btn, 0, 1)
        approval_buttons.addWidget(self.pass_btn, 1, 0)
        approval_buttons.addWidget(self.improve_btn, 1, 1)
        approval_layout.addLayout(approval_buttons)
        self._set_decision_enabled(False)

        # Improvement card (shown when user chooses to improve)
        self.improve_card = self._make_card("💡 Refine The Plan")
        self.improve_input = QtWidgets.QPlainTextEdit()
        self.improve_input.setPlaceholderText("Describe your suggestions for improvement...")
        self.improve_hint = QtWidgets.QLabel("This editor appears when you choose to improve an idea.")
        self.improve_hint.setWordWrap(True)
        self.improve_hint.setObjectName("hint")
        self.send_improve_btn = self._make_action_button("Send Feedback", "#88f2a8", "#0d2918")
        self.send_improve_btn.clicked.connect(self.send_improvement)
        self.improve_card.layout().addWidget(self.improve_input)
        self.improve_card.layout().addWidget(self.improve_hint)
        self.improve_card.layout().addWidget(self.send_improve_btn)
        self.improve_card.hide()

        # Controls
        controls = self._make_card("🎮 Control Panel")
        self.connection_hint = QtWidgets.QLabel("● Live connection active")
        self.connection_hint.setWordWrap(True)
        self.connection_hint.setObjectName("hint")
        self.stop_btn = self._make_action_button("Stop Backend", "#4ad7ff", "#041521")
        self.stop_btn.clicked.connect(self.stop_backend)
        controls.layout().addWidget(self.connection_hint)
        controls.layout().addWidget(self.stop_btn)

        right_layout.addWidget(self.portfolio_card)
        right_layout.addWidget(self.approval_card)
        right_layout.addWidget(self.improve_card)
        right_layout.addStretch(1)
        right_layout.addWidget(controls)

        app_layout.addWidget(left, 5)
        app_layout.addWidget(right, 3)

        # Connect buttons
        self.approve_btn.clicked.connect(lambda: self.send_decision("yes"))
        self.reject_btn.clicked.connect(lambda: self.send_decision("no"))
        self.pass_btn.clicked.connect(lambda: self.send_decision("pass"))
        self.improve_btn.clicked.connect(lambda: self.send_decision("improve"))

    def _make_pill(self, label: str, value: str):
        """Create a pill-shaped status indicator."""
        pill = QtWidgets.QFrame()
        pill.setStyleSheet(
            """
            QFrame {
              background: rgba(11, 20, 38, 0.92);
              border: 1px solid rgba(126, 160, 255, 0.18);
              border-radius: 12px;
              padding: 8px;
            }
            """
        )
        layout = QtWidgets.QHBoxLayout(pill)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        pill_label = QtWidgets.QLabel(label)
        pill_label.setObjectName("pillLabel")
        pill_value = QtWidgets.QLabel(value)
        pill_value.setObjectName("pillValue")

        layout.addWidget(pill_label)
        layout.addWidget(pill_value)
        return pill, pill_value

    def _make_card(self, title: str):
        """Create a card widget with title."""
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            """
            QFrame {
              background: rgba(11, 20, 38, 0.92);
              border: 1px solid rgba(126, 160, 255, 0.18);
              border-radius: 24px;
            }
            """
        )
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        card_title = QtWidgets.QLabel(title)
        card_title.setObjectName("cardTitle")
        layout.addWidget(card_title)

        return card

    def _make_action_button(self, text: str, bg: str, hover: str):
        """Create a styled action button."""
        btn = QtWidgets.QPushButton(text)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setStyleSheet(
            f"""
            QPushButton {{
              background: {bg};
              color: #07111f;
              border: none;
              border-radius: 10px;
              padding: 10px 18px;
              font-weight: 700;
              font-size: 12px;
            }}
            QPushButton:hover {{
              background: {hover};
            }}
            """
        )
        return btn

    def _apply_style(self):
        """Apply application-wide styles."""
        self.setStyleSheet(
            """
            QMainWindow {
              background: #07111f;
            }
            QFrame {
              background: rgba(11, 20, 38, 0.92);
              border: 1px solid rgba(126, 160, 255, 0.18);
              border-radius: 24px;
            }
            QLabel {
              color: #eef6ff;
            }
            QLabel#title {
              font-size: 30px;
              font-weight: 800;
              letter-spacing: 0.18em;
            }
            QLabel#subtitle, QLabel#hint {
              color: #8da2c9;
              font-size: 13px;
            }
            QLabel#pillLabel {
              color: #97a9c8;
              font-size: 10px;
              font-weight: 700;
              letter-spacing: 0.16em;
            }
            QLabel#pillValue {
              color: #f4fbff;
              font-size: 15px;
              font-weight: 800;
            }
            QLabel#cardTitle {
              color: #ffd166;
              font-size: 13px;
              font-weight: 800;
              letter-spacing: 0.12em;
            }
            QLabel#portfolioText, QLabel#approvalText {
              font-size: 13px;
              line-height: 1.5;
            }
            QLabel#spotlightTag {
              color: #6be8ff;
              font-size: 10px;
              font-weight: 700;
              letter-spacing: 0.2em;
              text-transform: uppercase;
            }
            QLabel#spotlightPhase {
              color: #f4fbff;
              font-size: 24px;
              font-weight: 800;
            }
            QLabel#spotlightTask {
              color: #a8b8d8;
              font-size: 14px;
              line-height: 1.6;
            }
            QListWidget {
              background: transparent;
              border: none;
              outline: none;
            }
            QPlainTextEdit {
              background: rgba(7, 17, 31, 0.8);
              border: 1px solid rgba(126, 160, 255, 0.18);
              border-radius: 12px;
              color: #eef6ff;
              padding: 10px;
              font-size: 13px;
            }
            QScrollBar:vertical {
              background: rgba(7, 17, 31, 0.6);
              width: 10px;
              border-radius: 5px;
            }
            QScrollBar::handle:vertical {
              background: rgba(126, 160, 255, 0.3);
              border-radius: 5px;
            }
            """
        )

    def _start_backend(self):
        """Start the backend shell script process."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "workgenerator.sh")

        if not os.path.exists(script_path):
            self._add_message("error", f"Backend script not found: {script_path}")
            return

        env = os.environ.copy()
        env["WORKGENERATOR_APP_GUI"] = "true"

        self.backend = subprocess.Popen(
            ["bash", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            env=env,
        )

        # Start reading output
        QtCore.QTimer.singleShot(100, self._read_backend_output)

    def _read_backend_output(self):
        """Read output from the backend process."""
        if self.backend is None:
            return

        try:
            line = self.backend.stdout.readline()
            if line:
                self._process_backend_line(line)
                QtCore.QTimer.singleShot(50, self._read_backend_output)
            elif self.backend.poll() is not None:
                self._add_message("system", "Backend process ended")
        except Exception as e:
            self._add_message("error", f"Backend read error: {str(e)}")

    def _process_backend_line(self, line: str):
        """Process a line from backend output."""
        line = line.strip()
        if not line:
            return

        # Check for GUI events
        if line.startswith("__WG_EVENT__|"):
            parts = line.split("|", 2)
            if len(parts) >= 2:
                event_type = parts[1]
                payload = base64.b64decode(parts[2]).decode() if len(parts) > 2 else ""
                self._handle_gui_event(event_type, payload)
            return

        # Regular output
        line = strip_ansi(line)
        if any(x in line.lower() for x in ["error", "failed", "exception"]):
            self._add_message("error", line)
        elif "decision" in line.lower() or "choice" in line.lower():
            self._add_message("assistant", line)
        else:
            self._add_message("log", line)

    def _handle_gui_event(self, event_type: str, payload: str):
        """Handle GUI events from backend."""
        if event_type == "PHASE":
            self.phase_value.setText(payload)
            self.spotlight_phase.setText(payload)
        elif event_type == "TASK":
            self.last_task = payload
            self.spotlight_task.setText(payload)
        elif event_type == "STATUS":
            self.status_value.setText(payload)
        elif event_type == "DECISION":
            self.pending_decision = payload
            self.approval_text.setText(payload)
            self._set_decision_enabled(True)
            self.improve_card.hide()
        elif event_type == "IMPROVEMENT_REQUEST":
            self.pending_improvement = True
            self.improve_card.show()
        elif event_type == "PORTFOLIO":
            self.portfolio_text.setText(payload)

    def _set_decision_enabled(self, enabled: bool):
        """Enable or disable decision buttons."""
        self.approve_btn.setEnabled(enabled)
        self.reject_btn.setEnabled(enabled)
        self.pass_btn.setEnabled(enabled)
        self.improve_btn.setEnabled(enabled)
        self.approval_card.start_glow() if enabled else self.approval_card.stop_glow()

    def _add_message(self, kind: str, text: str):
        """Add a message to the transcript."""
        self.messages.append((kind, text))
        if len(self.messages) > MAX_VISIBLE_MESSAGES:
            self.messages.popleft()

        item = QtWidgets.QListWidgetItem()
        widget = MessageWidget(kind, text)
        item.setSizeHint(widget.sizeHint())
        self.transcript_list.addItem(item)
        self.transcript_list.setItemWidget(item, widget)
        self.transcript_list.scrollToBottom()

    def send_decision(self, decision: str):
        """Send user decision to backend."""
        if self.backend and self.backend.poll() is None:
            self.backend.stdin.write(decision + "\n")
            self.backend.stdin.flush()
            self._set_decision_enabled(False)
            self._add_message("user", f"Decision: {decision}")

    def send_improvement(self):
        """Send improvement feedback to backend."""
        if self.backend and self.backend.poll() is None:
            text = self.improve_input.toPlainText()
            self.backend.stdin.write(text + "\n\n")
            self.backend.stdin.flush()
            self.improve_card.hide()
            self.improve_input.clear()
            self._add_message("user", f"Improvement: {text}")

    def stop_backend(self):
        """Stop the backend process."""
        if self.backend:
            self.backend.terminate()
            self.backend.wait()
            self._add_message("system", "Backend stopped by user")
            self.status_value.setText("Stopped")

    def closeEvent(self, event):
        """Handle window close event."""
        if self.backend:
            self.backend.terminate()
        event.accept()


def main():
    """Application entry point."""
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set application info
    app.setApplicationName("AI Work Generator Framework")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("vkumar-dev")

    window = WorkGeneratorDesktop()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
