import flet as ft
import flet_ads as fta


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # mobile-only
    supported = not page.web and page.platform.is_mobile()
    if supported:
        page.services.append(consent_manager := fta.ConsentManager())

    async def refresh_status():
        consent_status = await consent_manager.get_consent_status()
        privacy_status = await consent_manager.get_privacy_options_requirement_status()
        can_request = await consent_manager.can_request_ads()
        status.value = (
            f"Consent status: {consent_status.name}\n"
            f"Privacy options required: {privacy_status.name}\n"
            f"Can request ads: {can_request}"
        )
        # Only surface the privacy options entry point when we are required to.
        privacy_button.visible = (
            privacy_status == fta.PrivacyOptionsRequirementStatus.REQUIRED
        )
        page.update()

    async def gather_consent(e: ft.Event[ft.OutlinedButton]):
        status.value = "Gathering consent…"
        status.update()
        try:
            # Remember to remove the debug settings in production.
            await consent_manager.request_consent_info_update(
                fta.ConsentRequestParameters(
                    consent_debug_settings=fta.ConsentDebugSettings(
                        debug_geography=fta.DebugGeography.EEA,
                        # test_identifiers=["<HASHED_ID>"], # for physical devices only
                    ),
                )
            )
            # Loads and shows the consent form only if consent is required.
            await consent_manager.load_and_show_consent_form_if_required()
            await refresh_status()
            # At this point, if `can_request_ads()` is True, it is safe to start
            # loading ads (e.g. fta.BannerAd / fta.InterstitialAd).
        except Exception as ex:
            status.value = f"Error: {ex}"
            status.update()

    async def show_privacy_options(e: ft.Event[ft.OutlinedButton]):
        try:
            await consent_manager.show_privacy_options_form()
            await refresh_status()
        except Exception as ex:
            status.value = f"Error: {ex}"
        page.update()

    async def reset_consent(e: ft.Event[ft.OutlinedButton]):
        # For testing only: resets consent so you can replay the flow.
        try:
            await consent_manager.reset()
            status.value = 'Consent reset. Tap "Gather consent" to begin again.'
            privacy_button.visible = False
        except Exception as ex:
            status.value = f"Error: {ex}"
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Gather user consent (e.g. GDPR/EEA) with Google's User "
                        "Messaging Platform before requesting ads.",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.OutlinedButton(
                        content="Gather consent",
                        on_click=gather_consent,
                        disabled=not supported,
                    ),
                    privacy_button := ft.OutlinedButton(
                        content="Show privacy options form",
                        visible=False,
                        on_click=show_privacy_options,
                    ),
                    ft.OutlinedButton(
                        content="Reset consent (testing)",
                        on_click=reset_consent,
                        disabled=not supported,
                    ),
                    ft.Divider(),
                    status := ft.Text('Tap "Gather consent" to begin.'),
                ],
            )
        ),
    )


if __name__ == "__main__":
    ft.run(main)
