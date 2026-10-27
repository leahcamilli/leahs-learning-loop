---
title: "Building Real-Time Rail Tracking in Microsoft Fabric with KQL and Icon Map"
source: "https://www.linkedin.com/posts/jamesdales_microsoftfabric-iconmapforfabric-iconmap-ugcPost-7480152240335458304-2HDz/?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-07-09"
tags: [microsoft-fabric, kql, geospatial, realtime-intelligence, gtfs, mapping]
source_type: "web"
topics: [data-and-analytics]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Combine live vehicle positions with static route data so a tracking map shows not only where each train is, but also its route, destination, service status, and likely path through junctions. KQL supplies the enrichment logic, while Icon Map for Fabric turns the result into an interactive operational view.

## Key Takeaways

1. Join live coordinates to static routes, shapes, stops, destinations, and vehicle classes; coordinates alone cannot explain a train’s service or intended branch at a junction.
2. Use KQL to retain each vehicle’s latest event, join it to trip metadata, calculate operational states such as delayed or on time, and project map-ready fields.
3. Bind latitude and longitude to position, vehicle ID to the item key, route or status to color, destination and delay to tooltips, and train class to icon or 3D-model selection.
4. Treat the map as a decision surface by supporting train selection, tooltips, and filters for route, network, speed, or delay status.
5. Overlay stations, catchment areas, infrastructure, passenger loading, or reliability history to explain the operational significance of live vehicle positions.
6. According to the source, Icon Map for Fabric supports built-in 3D vehicle models and custom models stored in OneLake.
7. Reuse the same architecture—streaming telemetry, static network context, KQL enrichment, and interactive mapping—for buses, aircraft, delivery fleets, trams, or municipal vehicles.

## Overview

This lesson explains the architecture behind a real-time train tracking experience built in Microsoft Fabric using Realtime Intelligence, KQL, and Icon Map for Fabric. The source material describes a system that ingests both live vehicle positions and static route definitions, then visualizes moving trains on an interactive map with route-aware behavior, filtering, tooltips, and historical context.

This matters to engineers building operational dashboards, fleet monitoring systems, or geospatial analytics products. The same design pattern applies beyond rail: aircraft, buses, vans, trucks, trams, and other moving assets can all be tracked by combining streaming telemetry, static network data, and an interactive map layer that turns raw coordinates into operational insight.

## Key Concepts

- **Realtime Intelligence in Fabric**: Microsoft Fabric Realtime Intelligence provides the ingestion, query, and visualization foundations for streaming operational data. In this scenario, it enables live vehicle position updates to be queried with KQL and surfaced in a low-latency monitoring experience.
- **KQL for streaming geospatial analytics**: Kusto Query Language is well suited to filtering, aggregating, and enriching live telemetry. Engineers can use it to isolate delayed trains, compute reliability statistics, join position feeds with route metadata, and prepare map-friendly result sets.
- **GTFS static and realtime data**: GTFS-style transportation data typically comes in two forms: static schedule/route definitions and live position or trip updates. Combining both is essential because coordinates alone do not tell you which line a vehicle belongs to or how it should traverse complex junctions.
- **Route-aware map rendering**: A route-aware visualization does more than drop markers on latitude and longitude. It uses route and destination context from the static network files so trains can be shown moving along the correct corridor and branching correctly at junctions.
- **Interactive operational map layers**: The map is not just a display surface; it is a query and exploration tool. Users can select trains, inspect tooltips, filter by route or delay status, and overlay supporting layers such as stations, catchment areas, or infrastructure.
- **3D asset visualization from OneLake**: The source notes that the vehicle layer includes built-in 3D models and can also load custom models from OneLake. This allows different train classes or vehicle types to be represented with domain-specific visuals instead of generic map symbols.

## How It Works

At a high level, the system combines three data concerns and one presentation concern:

1. **Live vehicle positions** from a real-time feed.
2. **Static route/network definitions** describing lines, junctions, and destinations.
3. **Operational enrichment data** such as delays, reliability history, or passenger loading.
4. **An interactive geospatial layer** that renders vehicles and supports filtering and inspection.

The source describes a rail example using an in-house GTFS data source. The important idea is that a moving asset feed by itself is incomplete. A latitude/longitude pair tells you where a train is now, but not necessarily which branch it will take at a junction, what service it is operating, or how to color and classify it. By reading both the real-time positions feed and the static route files, the map can associate each train with its intended route and next destination.

A practical data flow looks like this:

- **Ingest static network data** such as routes, shapes, stops, service patterns, and train classes.
- **Ingest live position events** for trains, including identifiers, timestamps, coordinates, heading, speed, and trip references.
- **Join or enrich the events** using KQL so each incoming position is connected to route metadata, destination information, and operational status.
- **Prepare a map-ready result** containing geometry, labels, styling metadata, and optional model references.
- **Render the result in Icon Map for Fabric** with interactive behaviors such as selection, tooltips, and filtering.

The route-awareness is a key engineering detail. Transportation networks contain forks, parallel tracks, and overlapping services. If you only animate based on raw coordinates, the map can become visually misleading. When the system also knows the planned route and next destination, it can disambiguate movement across junctions and keep the visualization semantically correct.

The map experience itself is operationally rich rather than decorative. According to the source, users can:

- select individual trains
- view tooltips
- inspect reliability history
- inspect passenger loading
- filter to a route, network, or delayed vehicles
- combine train positions with other geospatial layers such as station catchments or infrastructure

This layering model is what makes geospatial telemetry useful in production. The moving vehicle layer provides the live state, while contextual layers explain why that state matters. For example, an engineer or operator could compare delayed trains against station areas, track assets, or historical trouble spots.

The mention of built-in and custom 3D models adds another implementation dimension. Instead of simple markers, the vehicle layer can represent different train classes with different visual assets. Storing uploaded models in OneLake makes them part of the broader Fabric data estate, which is useful for governance and reuse.

A minimal conceptual query pipeline in KQL might look like this:

```kusto
let StaticTrips = Trips
| project trip_id, route_id, destination, train_class;

let LivePositions = TrainPositions
| where Timestamp > ago(5m)
| summarize arg_max(Timestamp, *) by vehicle_id;

LivePositions
| join kind=leftouter StaticTrips on trip_id
| project vehicle_id, Timestamp, latitude, longitude, heading, speed,
          route_id, destination, train_class, delay_minutes
```

That result can then be bound to the map visual, where fields control:

- icon or 3D model selection
- tooltip contents
- color by route or delay status
- filters by network, route, or service health

The broader lesson is that this is a reusable real-time geospatial pattern:

- **stream telemetry** gives you freshness
- **static network data** gives you meaning
- **KQL enrichment** gives you operational logic
- **map interactivity** gives users a decision surface

Although the example is rail in Barcelona and Madrid, the same pattern extends naturally to planes from ADS-B feeds, buses from GTFS-realtime, delivery fleets, or municipal vehicles.

## Training Exercise

Build a simplified real-time transit tracking prototype in Fabric-style terms using static route metadata plus a simulated live positions table.

### Goal
Create a query that joins live train positions to route metadata, then produces a dataset suitable for an interactive map showing route, destination, and delay status.

### Step 1: Define a static metadata table
Create a small table or CSV with trip and route details:

```csv
trip_id,route_id,destination,train_class
T100,R1,Barcelona Sants,regional
T101,R2,Madrid Atocha,highspeed
T102,R1,Barcelona Sants,regional
```

### Step 2: Define a live positions table
Create or simulate a stream with records like:

```csv
vehicle_id,trip_id,timestamp,latitude,longitude,heading,speed,delay_minutes
V1,T100,2026-07-09T10:00:00Z,41.379,2.140,90,62,1
V2,T101,2026-07-09T10:00:05Z,40.416,-3.703,180,120,8
V3,T102,2026-07-09T10:00:10Z,41.385,2.173,45,55,0
```

### Step 3: Write a KQL enrichment query
Use a query similar to this:

```kusto
let StaticTrips = datatable(trip_id:string, route_id:string, destination:string, train_class:string)
[
  "T100", "R1", "Barcelona Sants", "regional",
  "T101", "R2", "Madrid Atocha", "highspeed",
  "T102", "R1", "Barcelona Sants", "regional"
];

let TrainPositions = datatable(vehicle_id:string, trip_id:string, Timestamp:datetime, latitude:real, longitude:real, heading:int, speed:int, delay_minutes:int)
[
  "V1", "T100", datetime(2026-07-09 10:00:00), 41.379, 2.140, 90, 62, 1,
  "V2", "T101", datetime(2026-07-09 10:00:05), 40.416, -3.703, 180, 120, 8,
  "V3", "T102", datetime(2026-07-09 10:00:10), 41.385, 2.173, 45, 55, 0
];

TrainPositions
| join kind=leftouter StaticTrips on trip_id
| extend status = case(delay_minutes >= 5, "delayed", delay_minutes > 0, "minor_delay", "on_time")
| project vehicle_id, Timestamp, latitude, longitude, route_id, destination, train_class, speed, heading, delay_minutes, status
```

### Step 4: Design the map fields
Prepare the output so a map visual can use:

- `latitude`, `longitude` for position
- `vehicle_id` as the item key
- `route_id` or `status` for color
- `destination`, `speed`, `delay_minutes` in the tooltip
- `train_class` to drive icon/model selection

### Step 5: Add basic operational filters
Create three filtered views or queries:

1. only delayed trains
2. only route `R1`
3. only trains above a speed threshold

Example:

```kusto
...
| where status == "delayed"
```

### Step 6: Extend the exercise
Add a station table with station coordinates and names, then think about how you would overlay it as a second map layer. As a stretch task, add a reliability metric per route and include it in the tooltip.

### What to learn from the exercise
By the end, you should be able to explain why live coordinates alone are not enough, how KQL enrichment turns telemetry into operational context, and how an interactive map becomes much more valuable when backed by both static network data and real-time updates.

## Test Yourself

<details><summary>Why are live latitude and longitude values insufficient for route-aware train tracking?</summary>

Coordinates identify a train’s current location but do not necessarily reveal its route, destination, service class, or intended branch at a junction. Joining the position feed to static network and trip metadata supplies that context.

</details>

<details><summary>What work should the KQL enrichment query perform before data reaches the map?</summary>

It should select the latest position per vehicle, join positions to static trip or route metadata, derive operational fields such as delay status, and return the geometry, labels, styling attributes, and tooltip values required by the map.

</details>

<details><summary>How can the prototype distinguish a delayed train and make that information useful to an operator?</summary>

A KQL `case` expression can classify a train with `delay_minutes >= 5` as `delayed`, while smaller positive values become `minor_delay`. The resulting status can drive map color, filtering, and tooltip details so operators can isolate affected services.

</details>

## Further Reading

- [Microsoft Fabric documentation](https://learn.microsoft.com/fabric/)
- [Kusto Query Language overview](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
- [General Transit Feed Specification (GTFS)](https://gtfs.org/)
- [GTFS Realtime reference](https://gtfs.org/documentation/realtime/reference/)
