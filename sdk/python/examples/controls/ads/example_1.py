import flet_ads as fta

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(
        adaptive=True,
        title="Mobile Ads Playground",
        bgcolor=ft.Colors.LIGHT_BLUE_300,
    )

    # Test ad unit IDs
    ids = {
        ft.PagePlatform.ANDROID: {
            "banner": "ca-app-pub-3940256099942544/6300978111",
            "interstitial": "ca-app-pub-3940256099942544/1033173712",
        },
        ft.PagePlatform.IOS: {
            "banner": "ca-app-pub-3940256099942544/2934735716",
            "interstitial": "ca-app-pub-3940256099942544/4411468910",
        },
    }

    def handle_interstitial_ad_close(e: ft.Event[fta.InterstitialAd]):
        nonlocal iad
        print("Closing InterstitialAd")
        page.overlay.remove(e.control)
        page.overlay.append(iad := get_new_interstitial_ad())
        page.update()

    async def handle_interstitial_ad_display(e: ft.Event[ft.OutlinedButton]):
        nonlocal iad
        print("Showing InterstitialAd")
        await iad.show()

    def get_new_interstitial_ad():
        return fta.InterstitialAd(
            unit_id=ids.get(page.platform, {}).get("interstitial"),
            on_load=lambda e: print("InterstitialAd loaded"),
            on_error=lambda e: print("InterstitialAd error", e.data),
            on_open=lambda e: print("InterstitialAd opened"),
            on_close=handle_interstitial_ad_close,
            on_impression=lambda e: print("InterstitialAd impression"),
            on_click=lambda e: print("InterstitialAd clicked"),
        )

    def get_new_banner_ad() -> ft.Container:
        return ft.Container(
            width=320,
            height=50,
            bgcolor=ft.Colors.TRANSPARENT,
            content=fta.BannerAd(
                unit_id=ids.get(page.platform, {}).get("banner"),
                on_click=lambda e: print("BannerAd clicked"),
                on_load=lambda e: print("BannerAd loaded"),
                on_error=lambda e: print("BannerAd error", e.data),
                on_open=lambda e: print("BannerAd opened"),
                on_close=lambda e: print("BannerAd closed"),
                on_impression=lambda e: print("BannerAd impression"),
                on_will_dismiss=lambda e: print("BannerAd will dismiss"),
            ),
        )

    page.overlay.append(iad := get_new_interstitial_ad())

    page.add(
        ft.OutlinedButton(
            content="Show InterstitialAd",
            on_click=handle_interstitial_ad_display,
        ),
        ft.OutlinedButton(
            content="Show BannerAd",
            on_click=lambda e: page.add(get_new_banner_ad()),
        ),
    )


ft.run(main)
