const TwitterSvg =
  '<svg style="fill: #1DA1F2; vertical-align: middle;" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z"></path></svg>';

const { themes } = require('prism-react-renderer');

module.exports = {
  title: 'Flet',
  tagline: 'Build multi-platform apps in Python',
  url: 'https://flet.dev',
  baseUrl: '/',
  favicon: 'img/favicon.ico',
  organizationName: 'flet-dev', // Usually your GitHub org/user name.
  projectName: 'flet', // Usually your repo name.
  customFields: {
    heroTitle: 'Build multi-platform apps in Python',
    heroSubTitle: 'Easily build realtime web, mobile and desktop apps in pure Python. No frontend experience required.',
  },
  themes: [
    'docusaurus-theme-github-codeblock'
  ],
  themeConfig: {
    // github codeblock theme configuration
    codeblock: {
      showGithubLink: true,
      githubLinkLabel: 'View on GitHub',
      showRunmeLink: false,
      runmeLinkLabel: 'Checkout via Runme'
    },
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      }
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    announcementBar: {
      id: 'announcementBar-2', // Increment on change
      content: `⭐️ If you like Flet, give it a star on <a target="_blank" rel="noopener noreferrer" href="https://github.com/flet-dev/flet">GitHub</a> and join the discussion on <a target="_blank" rel="noopener noreferrer" href="https://discord.gg/dzWXP8SHG8" >Discord</a>.`,
    },
    navbar: {
      hideOnScroll: true,
      title: 'Flet',
      logo: {
        alt: 'Flet Logo',
        src: 'img/logo.svg',
        srcDark: 'img/logo.svg',
      },
      items: [
        {
          to: 'https://docs.flet.dev',
          activeBasePath: 'docs',
          label: 'Docs',
          position: 'left',
        },
        {
          to: 'gallery',
          activeBasePath: 'gallery',
          label: 'Gallery',
          position: 'left',
        },
        {
          to: 'roadmap',
          activeBasePath: 'roadmap',
          label: 'Roadmap',
          position: 'left',
        },
        {
          to: 'blog',
          label: 'Blog',
          position: 'left'
        },
        {
          href: 'https://github.com/flet-dev/flet',
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        },
      ],
    },
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
      additionalLanguages: ['python', 'yaml', 'toml', 'bash', 'dart'],
    },
    footer: {
      style: 'light',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: 'https://docs.flet.dev',
            },
            {
              label: 'API Reference',
              to: 'https://docs.flet.dev/api-reference',
            }
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Discord',
              href: 'https://discord.gg/dzWXP8SHG8',
            },
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/flet',
            },
            {
              label: 'X',
              href: 'https://x.com/fletdev',
            },
            {
              label: 'Bluesky',
              href: 'https://bsky.app/profile/fletdev.bsky.social',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/flet-dev/flet',
            },
            {
              label: 'Support',
              href: '/support',
            },
          ],
        },
        {
          title: 'Legal',
          items: [
            {
              label: 'Privacy policy',
              to: 'privacy-policy',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Appveyor Systems Inc. Built with Docusaurus.`,
    },
    algolia: {
      apiKey: '4b060907ba79d92e8869e9d1ff80bce7',
      indexName: 'flet',
      appId: 'ESNSJEY7OD', // Optional, if you run the DocSearch crawler on your own
      algoliaOptions: {}, // Optional, if provided by Algolia
    }
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          // It is recommended to set document id as docs home page (`docs/` path).
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/flet-dev/website/edit/main/',
        },
        blog: {
          blogSidebarTitle: 'All posts',
          blogSidebarCount: 'ALL',
          postsPerPage: 5,
          showReadingTime: true,
          editUrl:
            'https://github.com/flet-dev/website/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
