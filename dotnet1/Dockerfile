# ---- Build stage ----
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY WeatherApi.csproj .
RUN dotnet restore

COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

# ---- Runtime stage ----
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app
COPY --from=build /app/publish .

# Listen on all interfaces, port 8080 (default non-root port in .NET 8+ images)
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

# Official aspnet images include a non-root "app" user
USER app

ENTRYPOINT ["dotnet", "WeatherApi.dll"]
