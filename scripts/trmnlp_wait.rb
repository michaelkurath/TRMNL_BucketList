# TRMNLP's PNG capture waits for page/fonts, but not the asynchronous framework
# layout pass. Wait for the framework's own completion flag before capturing.
# Loaded only by the QA runner; never uploaded as recipe markup.
require 'json'

module BucketListReadyCapture
  def capture(driver)
    Selenium::WebDriver::Wait.new(timeout: 30).until do
      driver.execute_script('return window.TRMNL_PLUGINS_READY === true')
    end
    driver.execute_async_script('const done = arguments[arguments.length - 1]; requestAnimationFrame(() => requestAnimationFrame(done));')
    metrics = driver.execute_script(<<~JS)
      const layout = document.querySelector('.layout');
      const bounds = layout.getBoundingClientRect();
      const items = [...document.querySelectorAll('.layout .item')].filter(e =>
        !e.closest('[data-staging]') && getComputedStyle(e).display !== 'none');
      return {
        screen: document.querySelector('.screen').className,
        view: document.querySelector('.view').className,
        layout: {top: bounds.top, bottom: bounds.bottom, left: bounds.left, right: bounds.right},
        items: items.map(e => {
          const r = e.getBoundingClientRect();
          const title = e.querySelector('.title');
          return {text: e.innerText, top: r.top, bottom: r.bottom, left: r.left, right: r.right,
                  titleSize: title ? getComputedStyle(title).fontSize : null,
                  clipped: r.top < bounds.top - 2 || r.bottom > bounds.bottom + 2 ||
                           r.left < bounds.left - 2 || r.right > bounds.right + 2};
        })
      };
    JS
    File.open('/plugin/qa-artifacts/geometry.jsonl', 'a') { |f| f.puts(JSON.generate(metrics)) }
    super
  end
end

# RUBYOPT loads this file before the trmnlp executable loads its application
# classes. Attach the wrapper as soon as Screenshot finishes being defined.
trace = TracePoint.new(:end) do
  next unless defined?(TRMNLP::Screenshot)

  TRMNLP::Screenshot.prepend(BucketListReadyCapture)
  trace.disable
end
trace.enable
