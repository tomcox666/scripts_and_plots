import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.StackPane;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public class WeatherRadar extends Application {

    private static final String OPENWEATHERMAP_API_KEY = "OPENWEATHERMAP_API_KEY";

    @Override
    public void start(Stage primaryStage) {
        WebView webView = new WebView();
        WebEngine webEngine = webView.getEngine();

        // Load Leaflet CSS and JavaScript files
        webEngine.loadContent("<!DOCTYPE html><html><head>"
                + "<link href='https://unpkg.com/leaflet@1.7.1/dist/leaflet.css' rel='stylesheet'>"
                + "<script src='https://unpkg.com/leaflet@1.7.1/dist/leaflet.js'></script>"
                + "<style>"
                + "#key {"
                + "position: absolute;"
                + "bottom: 10px;"
                + "left: 10px;"
                + "z-index: 1000;" // This line positions the key on top of the map
                + "background-color: white;"
                + "padding: 10px;"
                + "border: 1px solid black;"
                + "}"
                + "</style>"
                + "</head><body>"
                + "<div id='map' style='width: 100%; height: 100vh;'></div>"
                + "<div id='key'>"
                + "<h3>Precipitation Key:</h3>"
                + "<table>"
                + "<tr><td style='background-color: #ffffff; width: 20px; height: 20px;'></td><td>No precipitation</td></tr>"
                + "<tr><td style='background-color: #a0f2f2; width: 20px; height: 20px;'></td><td>Light precipitation</td></tr>"
                + "<tr><td style='background-color: #3e9cff; width: 20px; height: 20px;'></td><td>Moderate precipitation</td></tr>"
                + "<tr><td style='background-color: #3300ff; width: 20px; height: 20px;'></td><td>Heavy precipitation</td></tr>"
                + "</table>"
                + "</div>"
                + "<script>"
                + "var map = L.map('map').setView([43.7711, 11.2486], 8);"
                + "L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {"
                + "attribution: '&copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors',"
                + "}).addTo(map);"
                + "var precipitationLayer = L.tileLayer('https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=" + OPENWEATHERMAP_API_KEY + "&opacity=0.5&palette=1', {"
                + "tileSize: 256,"
                + "zoomOffset: -1"
                + "}).addTo(map);"
                + "</script>"
                + "</body></html>");

        StackPane root = new StackPane();
        root.getChildren().add(webView);

        Scene scene = new Scene(root, 800, 600);

        primaryStage.setTitle("Live Radar - Tuscany, Italy");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}