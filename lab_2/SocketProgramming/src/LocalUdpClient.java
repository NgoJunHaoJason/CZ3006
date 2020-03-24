import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

class LocalUdpClient {
    // server is lab server
    // private static final String LAB_SERVER_NAME = "SWL2-RM1-vL01";
    private static final String LOCAL_SERVER_IP_ADDRESS = "127.0.1.1";
    private static final int LOCAL_SERVER_PORT_NUMBER = 8000;

    private static final String CLIENT_IP_ADDRESS = "172.21.149.160";
    private static final int CLIENT_PORT_NUMBER = 8001;

    private static final String MY_NAME = "NgoJunHaoJason";
    private static final String LAB_GROUP = "TS1";

    private static byte[] buffer;

    public static void main(String[] args) {

        // 1. open UDP socket at well-known port
        DatagramSocket clientSocket = null;

        try {
            clientSocket = new DatagramSocket(CLIENT_PORT_NUMBER);

        } catch (SocketException socketException) {

            System.out.println(
                "Rfc865UdpClient SocketException: " + 
                socketException.getMessage()
            );

            System.out.println(
                "Stack Trace:\n" + 
                socketException.getStackTrace()
            );

            return;
        }

        String messageToSend = MY_NAME + ", " + LAB_GROUP + ", " + CLIENT_IP_ADDRESS;
        buffer = messageToSend.getBytes();

        try {
            // InetAddress serverAddress = InetAddress.getByName(LAB_SERVER_NAME);
            InetAddress serverAddress = InetAddress.getByName(LOCAL_SERVER_IP_ADDRESS);

            // 2. send UDP request to server
            DatagramPacket request = new DatagramPacket(
                buffer, 
                buffer.length,
                serverAddress,
                LOCAL_SERVER_PORT_NUMBER
            );
            clientSocket.send(request);

            // 3. receive UDP reply from server
            buffer = new byte[2048];
            DatagramPacket response = new DatagramPacket(buffer, buffer.length);
            clientSocket.receive(response);

            String messageReceived = new String(
                response.getData(), 
                response.getOffset(), 
                response.getLength()
            
                );
            System.out.println("From server: " + messageReceived);

        } catch (UnknownHostException unknownHostException) {

            System.out.println(
                "Rfc865UdpClient UnknownHostException: " + 
                unknownHostException.getMessage()
            );

            System.out.println(
                "Stack Trace:\n" + 
                unknownHostException.getStackTrace()
            );

        } catch (IOException ioException) {

            System.out.println(
                "Rfc865UdpClient IOException: " + 
                ioException.getMessage()
            );

            System.out.println(
                "Stack Trace:\n" + 
                ioException.getStackTrace()
            );
        } 

        if (clientSocket != null)
            clientSocket.close();
    }
}
