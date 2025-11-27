import os
from typing import Optional
from urllib.parse import urlparse

from .cli_to_md import render_flet_cli_as_markdown
from .controls_overview import render_controls_overview
from .iframe import render_iframe


def define_env(env):
    def format_value(value):
        if isinstance(value, bool):
            return str(value).lower()
        if value is None:
            return "null"
        return str(value)

    def build_options_lines(options, indent=8):
        lines = []
        prefix = " " * indent
        for key, value in options.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.extend(build_options_lines(value, indent + 4))
            else:
                lines.append(f"{prefix}{key}: {format_value(value)}")
        return lines

    def render_directive(class_name, options):
        lines = [f":::{class_name}", "    options:"]
        lines.extend(build_options_lines(options))
        return "\n".join(lines)

    @env.macro
    def class_all_options(
        class_name,
        separate_signature=True,
        **extra_options,
    ):
        options = {
            "show_root_toc_entry": True,
            "show_bases": True,
            "separate_signature": separate_signature,
            "extra": {
                "show_class_docstring": True,
                "show_children": True,
            },
            "summary": {
                "attributes": True,
                "functions": True,
            },
        }
        if extra_options:
            options.update(extra_options)
        block = render_directive(class_name, options)
        return f"{block}\n"

    @env.macro
    def image(src, alt=None, width=None, caption=None, link=None):
        if alt is None:
            parsed_src = urlparse(src)
            path = parsed_src.path or src
            filename = os.path.basename(path.rstrip("/"))
            alt_text = filename or src
        else:
            alt_text = alt
        alt_text = str(alt_text)
        body = f"![{alt_text}]({src})"
        if width:
            body += f'{{width="{width}"}}'
        if link:
            body = f"[{body}]({link})"
        caption_text = (caption or "").rstrip("\n")
        block = body + "\n/// caption\n"
        if caption_text:
            block += f"{caption_text}\n"
        block += "///"
        return block + "\n"

    @env.macro
    def class_summary(
        class_name,
        image_url=None,
        image_width="50%",
        image_caption=None,
        **options,
    ):
        summary_options = {
            "show_bases": True,
            "summary": {
                "attributes": True,
                "functions": True,
            },
        }
        base_options = {
            "show_root_toc_entry": True,
            "extra": {
                "show_class_docstring": True,
            },
        }
        if options:
            base_options.update(options)
        blocks = [render_directive(class_name, base_options)]
        if image_url:
            control_name = class_name.split(".")[-1]
            blocks.append(
                image(
                    image_url,
                    alt=control_name,
                    width=image_width,
                    caption=image_caption,
                ).rstrip("\n")
            )
        blocks.append(render_directive(class_name, summary_options))
        return "\n\n".join(blocks) + "\n"

    @env.macro
    def class_members(class_name):
        options = {
            "extra": {
                "show_children": True,
            },
        }
        return render_directive(class_name, options) + "\n"

    @env.macro
    def flet_cli_as_markdown(command: str = "", subcommands_only: bool = True):
        return render_flet_cli_as_markdown(
            command=command, subcommands_only=subcommands_only
        )

    @env.macro
    def controls_overview():
        return render_controls_overview()

    @env.macro
    def iframe(
        src=None,
        *,
        route=None,
        base="/apps/examples-gallery/dist/index.html#/",
        width="100%",
        height="480",
        title=None,
        allow=None,
        loading="lazy",
    ):
        return render_iframe(
            src=src,
            route=route,
            base=base,
            width=width,
            height=height,
            title=title,
            allow=allow,
            loading=loading,
        )

    @env.macro
    def demo(
        route_or_path: str,
        *,
        width: str = "100%",
        height: str = "350",
        title: Optional[str] = None,
    ):
        """
        Embed an examples gallery route as a centered demo iframe.

        `route_or_path` may be:
        - a gallery route, e.g. "slider/basic"
        - or a file path like "../../examples/controls/slider/basic.py"
        """
        route = route_or_path

        # Strip known prefixes
        for prefix in ("../../examples/controls/",):
            if route.startswith(prefix):
                route = route.removeprefix(prefix)
                break

        # Strip known suffixes
        for suffix in (".py", "/"):
            if route.endswith(suffix):
                route = route.removesuffix(suffix)
                break

        return render_iframe(
            route=route,
            base="/apps/examples-gallery/dist/index.html#/",
            width=width,
            height=height,
            title=title,
        )
