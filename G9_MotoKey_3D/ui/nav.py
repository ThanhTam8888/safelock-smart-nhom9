VIDEO_LINK='<a href="{href}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="m10 8 6 4-6 4z"/></svg>Video cách vận hành</a>'
def add_video_tab(html,href):
    return html.replace('</nav><div class="header-meta">',VIDEO_LINK.format(href=href)+'</nav><div class="header-meta">',1)
