import React, { useState } from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import CodeBlock from '@theme/CodeBlock';
import SignupForm from '@site/src/components/signup-form';
import styles from './styles.module.css';
const features = [{
  title: 'Good-looking Python GUIs',
  icon: 'controls',
  text: '150+ controls and services. Layouts, navigation, forms, and dialogs, with customizable colors, typography, and themes.',
  href: '/docs/controls',
  label: 'Explore the controls'
}, {
  title: 'Your Python libraries. On mobile.',
  icon: 'python-packages',
  text: 'Bring NumPy, pandas, Pillow, and cryptography along. Prebuilt packages for iOS and Android save you the work of compiling native dependencies.',
  href: '/docs/reference/binary-packages-android-ios',
  label: 'Browse Python packages'
}, {
  title: 'Ready to ship',
  icon: 'packaging',
  text: 'Package your app for desktop, mobile, and web with flet build. Prepare it for distribution, including the App Store and Google Play.',
  href: '/docs/publish',
  label: 'Build and publish'
}, {
  title: 'The web, your way',
  icon: 'web-support',
  text: 'Run Python in the browser with Pyodide and WebAssembly, or keep your code on a server and send real-time UI updates.',
  href: '/docs/publish/web',
  label: 'Explore web deployment'
}, {
  title: 'Test your app',
  icon: 'app-testing',
  text: 'Write pytest tests that tap buttons, enter text, and check user flows in your packaged app. Catch visual changes with screenshots on iOS and Android.',
  href: '/docs/getting-started/integration-testing',
  label: 'Test your app'
}, {
  title: 'Give your AI the right context',
  icon: 'ai-assistance',
  text: 'Connect your coding assistant to Flet MCP for version-specific API information and tools to find examples, icons, and CLI options.',
  href: '/docs/cookbook/flet-mcp',
  label: 'Connect Flet MCP'
}, {
  title: 'Make it your own',
  icon: 'extensible',
  text: 'Compose custom controls in Python or wrap Flutter packages in extensions to add new UI components and platform integrations.',
  href: '/docs/extend/user-extensions',
  label: 'Build an extension'
}, {
  title: 'Build for more people',
  icon: 'accessible',
  text: 'Support screen readers with labels and custom semantics. Add keyboard shortcuts and inspect the accessibility information your UI exposes.',
  href: '/docs/cookbook/accessibility',
  label: 'Explore accessibility'
}];
const examples = {
  imperative: `import flet as ft


def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def increment(e):
        counter.data += 1
        counter.value = str(counter.data)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment
    )
    page.add(
        ft.Container(
            content=counter,
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
    )


ft.run(main)`,
  declarative: `import flet as ft


@ft.component
def App():
    count, set_count = ft.use_state(0)

    return ft.View(
        floating_action_button=ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=lambda: set_count(count + 1),
        ),
        controls=[
            ft.Container(
                content=ft.Text(str(count), size=50),
                alignment=ft.Alignment.CENTER,
                expand=True,
            )
        ],
    )


ft.run(lambda page: page.render_views(App))`
};
function PlatformIcon({ platform }) {
  const iconBaseUrl = useBaseUrl('/img/pages/home/platforms/');
  if (platform === 'iOS') {
    return <svg viewBox="0 0 28 28" width="26" height="26" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <rect x="7" y="2" width="14" height="24" rx="3" />
      <path d="M12 5h4M13 23h2" />
    </svg>;
  }
  if (platform === 'Web') {
    return <svg viewBox="0 0 28 28" width="26" height="26" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <circle cx="14" cy="14" r="11" />
      <ellipse cx="14" cy="14" rx="5" ry="11" />
      <path d="M3 14h22M5 8h18M5 20h18" />
    </svg>;
  }
  const icon = platform.toLowerCase();
  return <span className={styles.platformIcon} style={{ '--platform-icon': `url("${iconBaseUrl}${icon}.svg")` }} aria-hidden="true" />;
}
function Arrow() {
  return <span aria-hidden="true">↗</span>;
}
function Feature({
  title,
  icon,
  text,
  href,
  label
}) {
  return <article className={styles.feature}>
      <img src={useBaseUrl(`/img/pages/home/${icon}.svg`)} alt="" width="40" height="40" loading="lazy" />
      <h3>{title}</h3>
      <p>{text}</p>
      <Link to={href}>{label} <Arrow /></Link>
    </article>;
}
function CodeExample() {
  const [mode, setMode] = useState('imperative');
  return <div className={styles.codeWindow}>
      <div className={styles.codeToolbar}>
        <span className={styles.fileName}>counter.py</span>
        <div className={styles.codeModes} role="group" aria-label="Programming style">
          {['imperative', 'declarative'].map(value => <button key={value} type="button" aria-pressed={mode === value} onClick={() => setMode(value)}>
              {value === 'imperative' ? 'Imperative' : 'Declarative'}
            </button>)}
        </div>
      </div>
      <div className={styles.codeExplanation}>
        <p aria-live="polite">{mode === 'imperative'
          ? 'Imperative: update the controls directly when the button is clicked.'
          : 'Declarative: update the count, and Flet rebuilds the interface to match.'}</p>
        <Link to="/docs/cookbook/declarative-vs-imperative">Compare the two styles <Arrow /></Link>
      </div>
      <CodeBlock language="python">{examples[mode]}</CodeBlock>
      <div className={styles.runCommand}><span aria-hidden="true">$</span> flet run counter.py</div>
    </div>;
}
export default function Home() {
  return <Layout title="Build cross-platform apps in Python" description="Build web, desktop, and mobile apps in Python. Start in your browser with Flet Studio, create reusable UI components, and ship your app across six platforms.">
      <main className={styles.home}>
        <section className={clsx(styles.shell, styles.hero)} aria-labelledby="hero-title">
          <div className={styles.heroCopy}>
            <Link className={styles.releaseLink} to="/blog/flet-1-0"><span className={styles.releaseDot} /> Meet Flet 1.0 <Arrow /></Link>
            <h1 id="hero-title">Your next app.<br />Built in <span>Python.</span></h1>
            <p className={styles.heroDescription}>Build beautiful web, desktop, and mobile apps from one Python codebase.</p>
            <div className={styles.actions}>
              <Link className={styles.primaryButton} to="https://studio.flet.dev">Try online <Arrow /></Link>
              <Link className={styles.secondaryButton} to="/docs">Read the docs <span aria-hidden="true">→</span></Link>
            </div>
            <p className={styles.heroNote}>No frontend experience required. Just Python.</p>
          </div>
          <div className={styles.heroVisual}>
            <div className={styles.desktopApp}>
              <div className={styles.windowBar}><span className={styles.windowDots} aria-hidden="true">● ● ●</span><span>My first Flet app</span><span aria-hidden="true">↗</span></div>
              <img src={useBaseUrl('/img/blog/declarative-ui/todo.png')} width="926" height="890" alt="A to-do app built with Flet, with editable tasks and completion filters" fetchPriority="high" />
            </div>
            <div className={styles.phoneApp}><img src={useBaseUrl('/docs/assets/getting-started/testing-on-mobile/ios/gallery.png')} width="1339" height="2716" alt="Flet Gallery running on an iPhone" /></div>
            <Link className={styles.visualCaption} to="https://github.com/flet-dev/awesome-flet">Real apps. All Python. <Arrow /></Link>
          </div>
        </section>

        <section className={clsx(styles.shell, styles.platforms)} aria-label="Supported platforms">
          <p>One codebase.<br /><strong>Make yourself at home.</strong></p>
          <ul>{['iOS', 'Android', 'Windows', 'macOS', 'Linux', 'Web'].map(platform => <li key={platform}><PlatformIcon platform={platform} /><span>{platform}</span></li>)}</ul>
        </section>

        <section className={clsx(styles.shell, styles.buildSection)} aria-labelledby="build-title">
          <div className={styles.buildCopy}>
            <span className={styles.eyebrow}>A SIMPLE EXAMPLE</span>
            <h2 id="build-title">Your first Flet app.</h2>
            <p>Start with a simple counter to see how Flet turns Python code into an interactive app.</p>
            <ol className={styles.exampleSteps}>
              <li><h3>Build the interface</h3><p>Use ready-made controls for the text and button. Arrange them with Python.</p></li>
              <li><h3>Add the behavior</h3><p>Connect the button to a Python function that increases the count.</p></li>
            </ol>
            <div className={styles.install}>
              <span>TRY IT YOURSELF</span>
              <div className={styles.tryOptions}>
                <div>
                  <Link className={styles.textLink} to="https://studio.flet.dev/gallery/getting-started/example/apps/templates/basic_counter">Try online <Arrow /></Link>
                  <p>Open Flet Studio.<br />No installation needed.</p>
                </div>
                <div>
                  <Link className={styles.textLink} to="/docs/getting-started/installation">Try locally <Arrow /></Link>
                  <p>Follow the installation guide for uv or pip.</p>
                </div>
              </div>
            </div>
          </div>
          <CodeExample />
        </section>

        <section className={clsx(styles.shell, styles.featuresSection)} aria-labelledby="features-title">
          <div className={styles.sectionHeading}><div><span className={styles.eyebrow}>BUILT FOR THE WHOLE JOURNEY</span><h2 id="features-title">More than a pretty interface.</h2></div><p>The controls, libraries, and tools to take your app from an experiment to something you ship.</p></div>
          <div className={styles.featureGrid}>{features.map(feature => <Feature key={feature.icon} {...feature} />)}</div>
        </section>

        <section className={clsx(styles.shell, styles.studioSection)} aria-labelledby="studio-title">
          <div className={styles.studioIntro}><span className={styles.eyebrow}>MEET FLET STUDIO</span><h2 id="studio-title">An idea is a<br />great place to start.</h2><p>Open your browser. Pick an example, write some Python, or ask the AI agent for a hand. Run your app and share what you make.</p><Link className={styles.primaryButton} to="https://studio.flet.dev">Create in Studio <Arrow /></Link><span className={styles.studioNote}>No installation required.</span></div>
          <div className={styles.studioSteps}>
            {[['01', 'Find your starting point', 'Explore the Gallery and make an example your own.'], ['02', 'Make it work your way', 'Edit the code, get help from AI, and see your app run.'], ['03', 'Share what you made', 'Send a link, or download your project and keep building locally.']].map(([number, title, text]) => <div key={number}><span>{number}</span><div><h3>{title}</h3><p>{text}</p></div></div>)}
            <Link to="https://studio.flet.dev/gallery">Explore the Gallery <Arrow /></Link>
          </div>
        </section>

        <section className={clsx(styles.shell, styles.community)} aria-labelledby="community-title"><div><span className={styles.eyebrow}>MADE BETTER, TOGETHER</span><h2 id="community-title">Your app. Our community.</h2><p>Share an idea, ask a question, or help shape what comes next. Flet is open source, and you're invited.</p></div><div className={styles.communityLinks}><Link to="https://github.com/flet-dev/flet">Contribute on GitHub <Arrow /></Link><Link to="https://discord.gg/dzWXP8SHG8">Join us on Discord <Arrow /></Link><Link to="https://github.com/flet-dev/awesome-flet">Discover community projects <Arrow /></Link></div></section>
        <div className={clsx(styles.shell, styles.newsletter)}><SignupForm /></div>
      </main>
    </Layout>;
}
