import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class UdpServer {
    private static final int PORT_NUMBER = 8000;
    private static final int BUFFER_LENGTH = 2048;

    private static byte[] buffer = new byte[BUFFER_LENGTH];

    public static void main(String[] args) {

        // 1. open UDP socket at well-known port
        DatagramSocket socket = null;

        try {
            InetAddress address = InetAddress.getLocalHost();
            System.out.println("Server address: " + address.toString());

            socket = new DatagramSocket(PORT_NUMBER, address);

        } catch (UnknownHostException unknownHostException) {

            System.out.println(
                "Rfc865UdpServer UnknownHostException: " + 
                unknownHostException.getMessage()
            );

            System.out.println(
                "Stack Trace:\n" + 
                unknownHostException.getStackTrace()
            );

            return;
        } catch (SocketException socketException) {

            System.out.println(
                "Rfc865UdpServer SocketException: " + 
                socketException.getMessage()
            );

            System.out.println(
                "Stack Trace:\n" + 
                socketException.getStackTrace()
            );

            return;
        }

        System.out.println("Listening for requests...");

        while (true) {

            try {
                // 2. listen for UDP request from client
                DatagramPacket request = new DatagramPacket(buffer, BUFFER_LENGTH);
                socket.receive(request);

                String messageReceived = new String(
                    request.getData(), 
                    request.getOffset(), 
                    request.getLength()
                );
                System.out.println("From client: " + messageReceived);

                String messageToSend = "Jason's computer received \"" + 
                    messageReceived + "\"";

                buffer = messageToSend.getBytes();

                InetAddress clientAddress = request.getAddress();
                int clientPort = request.getPort();

                // 3. send UDP reply to client
                DatagramPacket response = new DatagramPacket(
                    buffer, 
                    buffer.length,
                    clientAddress,
                    clientPort
                );
                socket.send(response);

                buffer = new byte[BUFFER_LENGTH];

            } catch (IOException ioException) {

                System.out.println(
                    "Rfc865UdpServer IOException: " + 
                    ioException.getMessage()
                );

                System.out.println(
                    "Stack Trace:\n" + 
                    ioException.getStackTrace()
                );

                break;
            } 
        }

        if (socket != null)
            socket.close();
    }
}
