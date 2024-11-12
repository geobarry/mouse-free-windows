from talon import Module, Context, clip, ctrl, cron, actions, canvas, screen, settings
from talon.windows import ax as ax, ui as winui
from talon.types import Point2d as Point2d
from talon.skia import  Paint

class element_highlights:
    def __init__(self):        
        self.canvas = canvas.Canvas.from_screen(winui.main_screen())
        self.canvas.register('draw', self.draw_canvas) 
        self.canvas.freeze() # uncomment this line for debugging
        self.rectangles = []
        self.labels = []
        self.job = cron.interval('100ms', self.check_for_updates)
        self.auto_highlight = False
        self.auto_label = False
        self.focused_rect = None
        self.focused_label = ""
    def check_for_updates(self):
        if self.auto_highlight:
            el = winui.focused_element()
            if el:
                if el.rect != self.focused_rect:
                    self.focused_rect = el.rect
                    if self.auto_label:
                        self.focused_label = el.name
                    self.canvas.move(0,0) # this forces canvas redraw
                if not self.auto_label:
                    if self.focused_label != "":
                        self.focused_label = ""
                        self.canvas.move(0,0) # this forces canvas redraw
            else:
                print("FUNCTION check_for_updates: unable to get focused element")
        else:
            if self.focused_rect != None:
                self.focused_rect = None
                self.focused_label = ""
                self.canvas.move(0,0)
    def add_element(self,rect,label = ''):
        self.rectangles.append(rect)
        self.labels.append(label)
        self.canvas.move(0,0) # this forces canvas redraw
    def remove_element(self,rect):
        try:
            idx = self.rectangles.index(rect)
            del self.rectangles[idx]
            del self.labels[idx]
            self.canvas.move(0,0) # this forces canvas redraw
        except:
            pass
        print(f"There are now {len(self.rectangles)} elements in highlight list")
    def clear_elements(self):
        self.rectangles = []
        self.labels = []
        self.canvas.move(0,0) # this forces canvas redraw
    def draw_canvas(self, canvas):
        print("redrawing canvas...")
        paint = canvas.paint
        paint.color = 'f3f'
        paint.style = paint.Style.STROKE
        paint.stroke_width = 7
        def highlight_element(rect,lbl,paint):
            canvas.draw_round_rect(rect,25,25,paint)
            # for now draw label below element
            
            if lbl != '':
                paint.stroke_width = 2
                if len(lbl) > 50:
                    lbl = lbl[:50]
                # determine label placement
                # assume text dimensions
                lbl_wd = 600
                lbl_ht = 30
                top_margin = rect.y
                btm_margin = canvas.height - rect.y - rect.height
                if top_margin > btm_margin:
                    y = max(rect.y - lbl_ht, 0)
                else:
                    y = min(rect.y + rect.height + 60, canvas.height - lbl_ht)
                x = min(rect.x,canvas.width - lbl_wd)
                print(f"*** {lbl} x = {x} | y = {y}")
                actions.user.text_aliased(lbl,x,y,46,canvas)        
        if len(self.rectangles) > 0:
            for idx in range(len(self.rectangles)):
                rect = self.rectangles[idx]
                lbl = self.labels[idx]
                highlight_element(rect,lbl,paint)
        if self.auto_highlight:
            # references to self.focused_element inside this function
            # will interfere with talon command canvas somehow, 
            # so we structure this so that we don't need to refer to 
            # self.focused_element here
            print("auto_highlight...")
            highlight_element(self.focused_rect,self.focused_label,paint)
    def disable(self):
        self.canvas.close()
        self.canvas = None
el_highlights = element_highlights()

mod = Module()
#
@mod.action_class
class Actions:
    def auto_highlight_scroll(amount: int):
        """Scrolls and then re highlights"""
        actions.mouse_scroll(amount)
        actions.user.clear_highlights()
        actions.sleep(0.5)
        actions.user.act_on_focused_element("highlight")
    def auto_highlight_on():
        """automatically highlight focused element"""
        el_highlights.auto_highlight = True
    def auto_highlight_off():
        """stop automatically highlighting focused element"""
        el_highlights.auto_highlight = False
    def auto_highlight_toggle():
        """toggle automatic highlighting of focused element"""
        el_highlights.auto_highlight = not el_highlights.auto_highlight
    def auto_label_on():
        """automatically highlight and label focused element"""
        el_highlights.auto_highlight = True  
        el_highlights.auto_label = True
    def auto_label_off():
        """turn off automatic labelling"""
        el_highlights.auto_label = False
    def highlight_element(el: ax.Element, lbl: str = ""):
        """Highlight specified element, with optional label"""
        rect = el.rect
        if len(lbl) > 50:
            lbl = lbl[:50]
        el_highlights.add_element(rect,lbl)
    def remove_highlight(el: ax.Element):
        """Remove element from highlights"""
        try:
            el_highlights.remove_element(el.rect)
        except:
            print("Unable to remove highlight: Element rectangle does not match any current highlight")
    def clear_highlights():
        """Removes all ui elements from the highlight list"""
        el_highlights.clear_elements()
    def key_highlight(keys: str, delay_before_highlight: float = 0.05, delay_after_highlight: float = 0):
        """Presses a key sequence and then highlights the focused element. If not forced, only highlights if in auto highlight mode."""
        actions.key(keys)
        if delay_before_highlight > 0:
            actions.sleep(delay_before_highlight)
        actions.user.clear_highlights()
        actions.user.highlight_element(winui.focused_element())
        if delay_after_highlight > 0:
            actions.sleep(delay_after_highlight)
        
