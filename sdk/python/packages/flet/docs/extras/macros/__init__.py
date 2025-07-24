def define_env(env):
    @env.macro
    def class_summary_and_description_options():
        return """
    options:
        show_root_heading: false
        show_bases: false
        members: false
        inherited_members: false
        show_root_toc_entry: false
        show_docstring_attributes: false
        show_docstring_functions: false
        show_docstring_examples: false
        show_docstring_parameters: false
        show_docstring_other_parameters: false
        show_docstring_raises: false
        show_docstring_receives: false
        show_docstring_returns: false
        show_docstring_warns: false
        show_docstring_yields: false
"""

    @env.macro
    def class_remove_summary_and_description_options():
        return """
    options:
        show_docstring_description: false
        show_labels: false
"""
