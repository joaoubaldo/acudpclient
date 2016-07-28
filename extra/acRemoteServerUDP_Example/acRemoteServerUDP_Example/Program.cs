using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace acRemoteServerUDP_Example {

    struct Vector3f {
        public float x, y, z;

        public override string ToString() {
            return "[" + x.ToString() + " , " + y.ToString() + " , " + z.ToString() + "]";
        }
    }


    class Program {

        static string readString(BinaryReader br) {
            // Read the length, 1 byte
            var length = br.ReadByte();

            // Read the chars
            return new string(br.ReadChars(length));

        }

        static string readStringW(BinaryReader br) {
            // Read the length, 1 byte
            var length = br.ReadByte();

            // Read the chars
            return Encoding.UTF32.GetString(br.ReadBytes(length * 4));

        }

        static void writeStringW(BinaryWriter bw, string message) {
            bw.Write((byte)(message.Length));

            bw.Write(Encoding.UTF32.GetBytes(message));
        }

        static void testSetSessionInfo(UdpClient client) {
            // Prepare the packet to send
            var buffer = new byte[1000];
            var bw = new BinaryWriter(new MemoryStream(buffer));

            // Packet ID
            bw.Write(ACSProtocol.ACSP_SET_SESSION_INFO);

            // Session Index we want to change, be very careful with changing the current session tho, some stuff might not work as expected
            byte session_index=1;
            bw.Write(session_index);

            // Session name
            writeStringW(bw,"SuperCoolServer"); // Careful here, the server is still broadcasting ASCII strings to the clients for this
            
            // Session type
            bw.Write((byte)3);

            // Laps
            bw.Write((UInt32)250);

            // Time (in seconds)
            bw.Write((UInt32)0);

            // Wait time (in seconds)
            bw.Write((UInt32)60);
            
            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 11000); // IP address of the server, with the port in UDP_PLUGIN_LOCAL_PORT in server_cfg

            client.Send(buffer, (int)bw.BaseStream.Length, ep);


        }

        static void testGetSessionInfo(UdpClient client) {
            // Prepare the packet to send
            var buffer = new byte[100];
            var bw = new BinaryWriter(new MemoryStream(buffer));

            // Packet ID
            bw.Write(ACSProtocol.ACSP_GET_SESSION_INFO);

            // Session index (-1 to request the current session)
            bw.Write((Int16)(-1));
                      

            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 11000); // IP address of the server, with the port in UDP_PLUGIN_LOCAL_PORT in server_cfg

            client.Send(buffer, (int)bw.BaseStream.Length, ep);
        }

        static void testGetCarInfo(UdpClient client, byte carID) {
            // Prepare the packet to send
            var buffer = new byte[100];
            var bw = new BinaryWriter(new MemoryStream(buffer));

            // Packet ID
            bw.Write(ACSProtocol.ACSP_GET_CAR_INFO);

            // The car ID we want to request about
            bw.Write(carID);

            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 11000); // IP address of the server, with the port in UDP_PLUGIN_LOCAL_PORT in server_cfg

            client.Send(buffer, (int)bw.BaseStream.Length, ep);

        }

        static void enableRealtimeReport(UdpClient client) {
            // Prepare the packet to send
            var buffer = new byte[100];
            var bw = new BinaryWriter(new MemoryStream(buffer));

            // Packet ID
            bw.Write(ACSProtocol.ACSP_REALTIMEPOS_INTERVAL);

            // Interval in MS
            bw.Write((UInt16)1000); // 1Hz

            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 11000); // IP address of the server, with the port in UDP_PLUGIN_LOCAL_PORT in server_cfg

            client.Send(buffer, (int)bw.BaseStream.Length,ep);


        }

        public static Vector3f readVector3f(BinaryReader br) {
            Vector3f res = new Vector3f();

            res.x = br.ReadSingle();
            res.y = br.ReadSingle();
            res.z = br.ReadSingle();

            return res;
        }



        public static void sendChat(UdpClient client,byte carid,string message) {
            // Prepare the packet to send
            var buffer = new byte[255];
            var bw = new BinaryWriter(new MemoryStream(buffer));

            // Packet ID
            bw.Write(ACSProtocol.ACSP_SEND_CHAT);

            // Car ID
            bw.Write(carid);

            // Message
            writeStringW(bw, message);

            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 11000); // IP address of the server, with the port in UDP_PLUGIN_LOCAL_PORT in server_cfg

            client.Send(buffer, (int)bw.BaseStream.Length, ep);

        }

        public static void broadcastChat(UdpClient client, string message) {
            // Prepare the packet to send
            var buffer = new byte[255];
            var bw = new BinaryWriter(new MemoryStream(buffer));

            // Packet ID
            bw.Write(ACSProtocol.ACSP_BROADCAST_CHAT);
                     

            // Message
            writeStringW(bw, message);

            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 11000); // IP address of the server, with the port in UDP_PLUGIN_LOCAL_PORT in server_cfg

            client.Send(buffer, (int)bw.BaseStream.Length, ep);

        }

        public static void testKick(UdpClient client, byte userid) {
            // Prepare the packet to send
            var buffer = new byte[255];
            var bw = new BinaryWriter(new MemoryStream(buffer));

            // Packet ID
            bw.Write(ACSProtocol.ACSP_KICK_USER);
            bw.Write(userid);
                       
            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 11000); // IP address of the server, with the port in UDP_PLUGIN_LOCAL_PORT in server_cfg

            client.Send(buffer, (int)bw.BaseStream.Length, ep);
        }

        static void Main(string[] args) {

            IPEndPoint ep = new IPEndPoint(IPAddress.Any, 12000);
            var client = new UdpClient(ep);

            while (true) {

                var src_ep = new IPEndPoint(IPAddress.Any,0);

                var bytes=client.Receive(ref src_ep);

                var br = new BinaryReader(new MemoryStream(bytes));

                var packet_id = br.ReadByte();
                Console.WriteLine("PACKET ID:" + packet_id);
                switch (packet_id) {
                    case ACSProtocol.ACSP_ERROR: {
                            var msg = readStringW(br);

                            Console.WriteLine(msg);
                        }
                        break;
                    case ACSProtocol.ACSP_CHAT: {
                            var car_id = br.ReadByte();
                            var msg = readStringW(br);

                            Console.WriteLine("CHAT FROM CAR:" + (int)car_id + " MSG:" + msg);
                        }
                        break;
                    case ACSProtocol.ACSP_CLIENT_LOADED: {
                            var car_id = br.ReadByte();

                            Console.WriteLine("CLIENT LOADED:" + (int)car_id);

                        }
                        break;

                    case ACSProtocol.ACSP_VERSION:
                        var protocol_version = br.ReadByte();

                        Console.WriteLine("PROTOCOL VERSION IS:" + (int)protocol_version);
                        break;
                    case ACSProtocol.ACSP_NEW_SESSION:
                        Console.WriteLine("New session started");
                        goto case ACSProtocol.ACSP_SESSION_INFO;
                    case ACSProtocol.ACSP_SESSION_INFO:
                        Console.WriteLine("Session Info");

                        var version = br.ReadByte(); // UDP Plugin protocol version, in case you miss the first ACSP_VERSION message sent by the server at startup
                        var sess_index = br.ReadByte(); // The index of the session in the message
                        var current_session_index = br.ReadByte(); // The index of the current session in the server
                        var session_count = br.ReadByte(); // The number of sessions in the server
                        
                        
                        var server_name = readStringW(br);
                        var track = readString(br);
                        var track_config = readString(br);
                        var name = readString(br);
                        var type = br.ReadByte();
                        var time = br.ReadUInt16();
                        var laps = br.ReadUInt16();
                        var waitTime = br.ReadUInt16();
                        var ambient_temp = br.ReadByte();
                        var road_temp = br.ReadByte();
                        var weather_graphics = readString(br);
                        var elapsedMS = br.ReadInt32(); // Milliseconds from the start (this might be negative for races with WaitTime)

                        Console.WriteLine("PROTOCOL VERSION:" + version);
                        Console.WriteLine("SESSION INDEX:" + sess_index + "/" + session_count + " CURRENT SESSION:" + current_session_index);
                        Console.WriteLine("SERVER NAME:" + server_name);
                        Console.WriteLine("TRACK:" + track+" ["+track_config+"]");
                        Console.WriteLine("NAME:"+name);
                        Console.WriteLine("TYPE:" + type);
                        Console.WriteLine("TIME:" + time);
                        Console.WriteLine("LAPS:" + laps);
                        Console.WriteLine("WAIT TIME:" + waitTime);
                        Console.WriteLine("WEATHER:" + weather_graphics + " AMBIENT:" + ambient_temp + " ROAD:" + road_temp);
                        Console.WriteLine("ELAPSED:" + elapsedMS);

                        if (packet_id == ACSProtocol.ACSP_NEW_SESSION) {
                            // UNCOMMENT to enable realtime position reports
                            enableRealtimeReport(client);

                            // TEST ACSP_GET_CAR_INFO
                            testGetCarInfo(client, 2);

                            sendChat(client, 0, "CIAO BELLO!");
                            broadcastChat(client, "E' arrivat' 'o pirit'");

                            // Test Kick User, bad index, it will also trigger an error
                            testKick(client, 230);
                        }
                        break;
                    case ACSProtocol.ACSP_END_SESSION:
                        Console.WriteLine("ACSP_END_SESSION");
                        var filename = readStringW(br);

                        Console.WriteLine("REPORT JSON AVAILABLE AT:" + filename);

                        break;
                    case ACSProtocol.ACSP_CLIENT_EVENT: {
                        var ev_type = br.ReadByte();
                        var car_id = br.ReadByte();
                        byte other_car_id = 255;

                        switch (ev_type) {
                            case ACSProtocol.ACSP_CE_COLLISION_WITH_CAR:
                                other_car_id=br.ReadByte();

                                break;
                            case ACSProtocol.ACSP_CE_COLLISION_WITH_ENV:
                                
                                break;
                        }

                        var speed=br.ReadSingle(); // Impact speed
                        var world_pos=readVector3f(br);
                        var rel_pos=readVector3f(br);

                        switch (ev_type) {
                            case ACSProtocol.ACSP_CE_COLLISION_WITH_ENV:
                                Console.WriteLine("COLLISION WITH ENV, CAR:"+car_id+" IMPACT SPEED:"+speed+" WORLD_POS:"+world_pos.ToString()+" REL_POS:"+rel_pos.ToString());
                                break;
                            case ACSProtocol.ACSP_CE_COLLISION_WITH_CAR:
                                 Console.WriteLine("COLLISION WITH CAR, CAR:"+car_id+" OTHER CAR:"+other_car_id+" IMPACT SPEED:"+speed+" WORLD_POS:"+world_pos.ToString()+" REL_POS:"+rel_pos.ToString());
                                break;

                        }
                    }
                        break;
                    case ACSProtocol.ACSP_CAR_INFO: {
                        Console.WriteLine("ACSP_CAR_INFO");

                        var car_id = br.ReadByte(); // The server resends the Id so we can handle many requests at the time and still understand who we are talking about
                        var is_connected = br.ReadByte() != 0; // Is the car currently attached to a connection?
                        var model = readStringW(br);
                        var skin = readStringW(br);
                        var driver_name = readStringW(br);
                        var driver_team = readStringW(br);
                        var driver_guid = readStringW(br);

                        Console.WriteLine("CAR:" + car_id + " " + model + " [" + skin + "] DRIVER:" + driver_name + " TEAM:" + driver_team + " GUID:" + driver_guid+" CONNECTED:"+is_connected);

                        // TEST GET SESSION INFO. This will generate a loop of messages!
                        // testGetSessionInfo(client);
                        testSetSessionInfo(client);
                        }
                        break;
                    case ACSProtocol.ACSP_CAR_UPDATE: {
                        Console.WriteLine("ACSP_CAR_UPDATE");

                        var car_id = br.ReadByte();
                        var pos = readVector3f(br);
                        var velocity = readVector3f(br);
                        var gear = br.ReadByte();
                        var engine_rpm = br.ReadUInt16();
                        var normalized_spline_pos = br.ReadSingle();

                        Console.Write("CAR:" + car_id + " POS:" + pos.ToString() + " VEL:" + velocity.ToString() + " GEAR:" + gear + " RPM:" + engine_rpm+" NSP:"+normalized_spline_pos);

                        }
                        break;
                    case ACSProtocol.ACSP_NEW_CONNECTION: {
                            Console.WriteLine("ACSP_NEW_CONNECTION");

                            var driver_name = readStringW(br);
                            var driver_guid = readStringW(br);
                            var car_id = br.ReadByte();
                            var car_model = readString(br);
                            var car_skin = readString(br);
                            Console.WriteLine("DRIVER:" + driver_name + " GUID:" + driver_guid);
                            Console.WriteLine("CAR:" + car_id + " MODEL:" + car_model + " SKIN:" + car_skin);

                            // Test ACSP_GET_CAR_INFO with a connected car (it will still report connected=False because by the time we get this notification the client is still loading)
                            testGetCarInfo(client, car_id);
                        }
                        break;
                    case ACSProtocol.ACSP_CONNECTION_CLOSED: {
                            Console.WriteLine("ACSP_CONNECTION_CLOSED");

                            var driver_name = readStringW(br);
                            var driver_guid = readStringW(br);
                            var car_id = br.ReadByte();
                            var car_model = readString(br);
                            var car_skin = readString(br);
                            Console.WriteLine("DRIVER:" + driver_name + " GUID:" + driver_guid);
                            Console.WriteLine("CAR:" + car_id + " MODEL:" + car_model + " SKIN:" + car_skin);
                        }
                        break;
                    case ACSProtocol.ACSP_LAP_COMPLETED: {
                            Console.WriteLine("ACSP_LAP_COMPLETED");

                            var car_id = br.ReadByte();
                            var laptime = br.ReadUInt32();
                            var cuts = br.ReadByte();
                            Console.WriteLine("CAR:" + car_id + " LAP:" + laptime + " CUTS:" + cuts);

                            var cars_count = br.ReadByte();
                            
                            // LEADERBOARD
                            for (int i = 0; i < cars_count; i++) {
                                var rcar_id = br.ReadByte();
                                var rtime = br.ReadUInt32();
                                var rlaps = br.ReadUInt16();

                                Console.WriteLine((i + 1).ToString() + ": CAR_ID:" + rcar_id + " TIME:" + rtime + " LAPS:" + rlaps);
                            }

                            var grip_level = br.ReadSingle();

                            Console.WriteLine("GRIP LEVEL:" + grip_level);
                        }
                        break;

                }


            }
        
        
        
        }
    }
}
