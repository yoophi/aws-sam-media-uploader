# aws-sam-media-uploader

## Sequence Diagram

```mermaid
sequenceDiagram
  autonumber
  
  actor User 
  participant APIA as API
  participant WS as WebSocket
  participant API as Internal API
  participant B1 as Upload Bucket
  participant Event as EventBridge
  participant EventHandler
  participant B2 as Persist Bucket
  participant DB as Database

  User->>+APIA: want to upload file
  APIA->>+API: request presigned url with apikey<br>with userId and contexts
  API->>+B1: request presigned url
  B1->>-API: presigned url
  API->>-APIA: presigned url<br>with websocket url
  APIA->>-User: presigned url
  User->>+B1: upload w/ presigned url
  User-->>WS: subscribe to websocket
  B1->>-User: upload completed
  B1->>Event: new file
  Event->>EventHandler: handle event
  activate EventHandler
  EventHandler->>B1: get file
  B1->>EventHandler: file

  alt if filePath is valid
    EventHandler->>B2: upload file
    B2->>EventHandler: 
    EventHandler->>DB: save data based on path
    DB->>EventHandler: 
    EventHandler->>+WS: file upload finished
    deactivate EventHandler
    WS-->>-User: send file upload success message
  end
  ```
