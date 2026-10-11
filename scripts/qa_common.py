"""Interaction checks shared by local and deployed viewer QA."""

def check_display(page, section, source, clipboard=False):
    graph = section.get_by_role('tab', name='Graph', exact=True)
    code = section.get_by_role('tab', name='Code', exact=True)
    graph.focus()
    page.keyboard.press('ArrowRight')
    assert code.get_attribute('aria-selected') == 'true'
    assert code.evaluate('(e)=>e===document.activeElement')
    assert section.locator('.code-panel').is_visible()
    assert not section.locator('.graph-panel').is_visible()
    assert section.locator('code').text_content() == source, 'Code must equal exact authored file, including whitespace'
    assert section.locator('code span[class^="hljs-"]').count() > 0, 'Official syntax highlighting present'
    assert page.locator('#in').is_disabled()
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Code must scroll within its own frame'
    if clipboard:
        section.locator('.copy-code').click()
        page.wait_for_function("document.querySelector('.episode:not([hidden]) .copy-status').textContent==='Copied.'")
        assert page.evaluate('navigator.clipboard.readText()') == source, 'Clipboard must contain actual source'
    code.focus()
    page.keyboard.press('Home')
    assert graph.get_attribute('aria-selected') == 'true'
    assert section.locator('.graph-panel').is_visible()
    assert not page.locator('#in').is_disabled()
    page.keyboard.press('End')
    assert code.get_attribute('aria-selected') == 'true'
    page.keyboard.press('ArrowLeft')
    assert graph.get_attribute('aria-selected') == 'true'


def check_copy_fallback(page, section, source):
    section.get_by_role('tab', name='Code', exact=True).click()
    page.evaluate('''()=>{
      window.savedClipboard=Object.getOwnPropertyDescriptor(navigator,'clipboard');
      window.savedExecCommand=document.execCommand;
      Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('Denied for fallback test')}}});
      document.execCommand=()=>false;
    }''')
    section.locator('.copy-code').click()
    page.wait_for_function("document.querySelector('.episode:not([hidden]) .copy-status').textContent.includes('Source selected.')")
    field=section.locator('.copy-fallback')
    assert field.input_value()==source
    assert field.evaluate('(e)=>e.selectionStart===0 && e.selectionEnd===e.value.length && e===document.activeElement')
    page.evaluate('''()=>{
      if(window.savedClipboard)Object.defineProperty(navigator,'clipboard',window.savedClipboard);else delete navigator.clipboard;
      document.execCommand=window.savedExecCommand;getSelection().removeAllRanges();
    }''')
    section.get_by_role('tab', name='Graph', exact=True).click()
