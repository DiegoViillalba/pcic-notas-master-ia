import { PageFrame, PageFrameProps } from "./types"
import HeaderConstructor from "../Header"

const Header = HeaderConstructor()

/**
 * The default page frame — three-column layout with left sidebar, center
 * content (header + body + afterBody), and right sidebar, followed by a footer.
 *
 * This is the original Quartz layout, extracted from renderPage.tsx.
 */
export const DefaultFrame: PageFrame = {
  name: "default",
  render({
    componentData,
    header,
    beforeBody,
    pageBody: Content,
    afterBody,
    left,
    right,
    footer,
  }: PageFrameProps) {
    return (
      <>
        <div class="left sidebar">
          {left.map((BodyComponent) => (
            <BodyComponent {...componentData} />
          ))}
        </div>
        <div class="center">
          <div class="page-header">
            <Header {...componentData}>
              {header.map((HeaderComponent) => (
                <HeaderComponent {...componentData} />
              ))}
            </Header>
            <div class="popover-hint">
              {beforeBody.map((BodyComponent) => (
                <BodyComponent {...componentData} />
              ))}
            </div>
          </div>
          <Content {...componentData} />
          <hr />
          <div class="page-footer">
            {afterBody.map((BodyComponent) => (
              <BodyComponent {...componentData} />
            ))}
          </div>
        </div>
        <div class="right sidebar">
          <button
            id="right-sidebar-toggle"
            class="right-sidebar-toggle"
            type="button"
            title="Colapsar/expandir barra lateral"
            aria-label="Colapsar barra lateral derecha"
            aria-expanded="true"
          >
            <svg
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
          {right.map((BodyComponent) => (
            <BodyComponent {...componentData} />
          ))}
        </div>
        {footer.map((FooterComponent) => (
          <FooterComponent {...componentData} />
        ))}
        <script
          // eslint-disable-next-line react/no-danger
          dangerouslySetInnerHTML={{
            __html: `(function(){
  var KEY = "quartz-right-sidebar-collapsed";
  function apply(collapsed) {
    var body = document.getElementById("quartz-body");
    if (!body) return;
    body.classList.toggle("right-collapsed", collapsed);
    var btn = document.getElementById("right-sidebar-toggle");
    if (btn) btn.setAttribute("aria-expanded", String(!collapsed));
  }
  function onClick() {
    var body = document.getElementById("quartz-body");
    if (!body) return;
    var next = !body.classList.contains("right-collapsed");
    localStorage.setItem(KEY, String(next));
    apply(next);
  }
  function init() {
    apply(localStorage.getItem(KEY) === "true");
    var btn = document.getElementById("right-sidebar-toggle");
    if (btn && !btn.dataset.bound) {
      btn.dataset.bound = "true";
      btn.addEventListener("click", onClick);
    }
  }
  document.addEventListener("nav", init);
})();`,
          }}
        />
      </>
    )
  },
}
