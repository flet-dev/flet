import flet
from flet import Persona

page = flet.page("persona-test")
page.add(Persona("Jack Reacher", secondary_text="Designed", size=8))
page.add(Persona("John Smith", secondary_text="Student", size=24))
page.add(Persona("Marry Poppins", size=32, presence="busy", hide_details=True))
page.add(
    Persona(
        "Feodor",
        size=32,
        image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        presence="online",
    )
)
page.add(Persona("Alice Brown", size=72, secondary_text="Wonderer"))
