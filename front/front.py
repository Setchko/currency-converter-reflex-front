import reflex as rx
import requests

class State(rx.State):
    """El estado de la aplicación para el convertidor de monedas."""
    from_currency: str = "USD"
    to_currency: str = "EUR"
    amount: float = 1.0
    result: float = 0.0

    currencies: list[str] = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"]

    def convert(self):
        """Función para realizar la conversión usando el backend de FastAPI."""
        if self.amount <= 0:
            return rx.window_alert("La cantidad debe ser mayor que 0")

        try:
            response = requests.get(
                "http://localhost:8000/convert",
                params={
                    "from_currency": self.from_currency,
                    "to_currency": self.to_currency,
                    "amount": self.amount,
                }
            )
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    rx.window_alert(data["error"])
                    self.result = 0
                else:
                    self.result = data["result"]
            else:
                print(f"Error: {response.status_code}")
                self.result = 0
        except requests.RequestException as e:
            print(f"Error en la petición: {e}")
            self.result = 0

def index():
    """La UI principal del convertidor de monedas."""
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "Convertidor de Monedas",
                    size="4",  # Cambiado de size="6" a "4"
                    color="blue.500",
                    padding_bottom="4",
                ),
                rx.hstack(
                    rx.select(
                        State.currencies,
                        placeholder="Desde",
                        value=State.from_currency,
                        on_change=State.set_from_currency,
                        color="gray.800",
                        border_color="blue.200",
                        _hover={"border_color": "blue.500"},
                        width="150px",
                    ),
                    rx.icon(
                        tag="arrow_right",
                        color="blue.500",
                        font_size="xl",
                    ),
                    rx.select(
                        State.currencies,
                        placeholder="Hasta",
                        value=State.to_currency,
                        on_change=State.set_to_currency,
                        color="gray.800",
                        border_color="blue.200",
                        _hover={"border_color": "blue.500"},
                        width="150px",
                    ),
                    spacing="4",
                ),
                rx.input(
                    type="number",
                    value=State.amount,
                    on_change=State.set_amount,
                    min=0,
                    border_color="blue.200",
                    _hover={"border_color": "blue.500"},
                    width="320px",
                    padding="2",
                    margin_y="4",
                ),
                rx.button(
                    "Convertir",
                    on_click=State.convert,
                    color="white",
                    padding_x="8",
                    padding_y="2",
                    _hover={"bg_color": "blue.600"},
                    border_radius="lg",
                ),
                rx.box(
                    rx.text(
                        "Resultado:",
                        font_weight="bold",
                        color="gray.600",
                    ),
                    rx.heading(
                        f"{State.result}",
                        size="5",  # Cambiado de "lg" a "5"
                        color="blue.500",
                    ),
                    padding="4",
                    border_radius="lg",
                    margin_top="4",
                ),
                spacing="3",
                width="100%",
            ),
            padding="8",
            border_radius="xl",
            box_shadow="lg",
            width="400px",
        ),
        width="100%",
        min_height="100vh",
    )

app = rx.App()
app.add_page(index)