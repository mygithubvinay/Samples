var builder = WebApplication.CreateBuilder(args);

// Allow calls from any origin (browsers, other apps, anywhere)
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
        policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod());
});

builder.Services.AddOpenApi();

var app = builder.Build();

app.UseCors();

app.MapOpenApi(); // OpenAPI JSON at /openapi/v1.json

// Sample in-memory data
string[] summaries = ["Freezing", "Cold", "Cool", "Mild", "Warm", "Hot", "Scorching"];
string[] cities = ["London", "New York", "Tokyo", "Mumbai", "Amsterdam", "Sydney"];

WeatherReading MakeReading(string city, DateOnly date)
{
    var rng = Random.Shared;
    var tempC = rng.Next(-5, 40);
    return new WeatherReading(
        city,
        date,
        tempC,
        32 + (int)(tempC / 0.5556),
        rng.Next(20, 95),
        summaries[Math.Clamp((tempC + 10) / 8, 0, summaries.Length - 1)]);
}

app.MapGet("/", () => Results.Ok(new { service = "Weather API", status = "running" }));

app.MapGet("/health", () => Results.Ok("healthy"));

// GET /weather  -> current weather for all sample cities
app.MapGet("/weather", () =>
    cities.Select(c => MakeReading(c, DateOnly.FromDateTime(DateTime.UtcNow))));

// GET /weather/Tokyo  -> current weather for one city
app.MapGet("/weather/{city}", (string city) =>
    Results.Ok(MakeReading(city, DateOnly.FromDateTime(DateTime.UtcNow))));

// GET /weather/Tokyo/forecast?days=5  -> simple forecast
app.MapGet("/weather/{city}/forecast", (string city, int days = 5) =>
{
    days = Math.Clamp(days, 1, 14);
    var today = DateOnly.FromDateTime(DateTime.UtcNow);
    return Enumerable.Range(1, days).Select(i => MakeReading(city, today.AddDays(i)));
});

app.Run();

record WeatherReading(
    string City,
    DateOnly Date,
    int TemperatureC,
    int TemperatureF,
    int HumidityPercent,
    string Summary);
