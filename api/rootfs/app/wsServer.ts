import { WebSocket, isWebSocketCloseEvent } from "https://deno.land/std@0.99.0/ws/mod.ts";

let connections = new Array;

export const handleSocket = async (ws: WebSocket): Promise<void> =>{
    console.log("Websocket connection established")
    connections.push(ws);
    for await (const event of ws){
        if(isWebSocketCloseEvent(event)){
            connections = connections.filter(websocket => websocket !== ws)
            console.log("Websocket connection closed")
        }
    }
}

export const broadcastEvents = (event: string) =>{
    for(const websocket of connections){
        websocket.send(event);
    }
}