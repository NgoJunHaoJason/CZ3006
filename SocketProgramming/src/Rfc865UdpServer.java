import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class Rfc865UdpServer {
    // quote of the day protocol

    private static final int PORT_NUMBER = 8000; // RFC865
    private static final int QUOTE_LENGTH = 512; // RFC865
    private static final String END_MESSAGE = "end";

    // buffer size of 2048 should be more than enough
    private static byte[] readBuffer = new byte[QUOTE_LENGTH];
    private static byte[] writeBuffer = new byte[QUOTE_LENGTH];

    public static void main(String[] args) {

        // 1. open UDP socket at well-known port
        DatagramSocket socket = null;

        try {
            InetAddress address = InetAddress.getLocalHost();
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

        while (true) {

            try {
                // 2. listen for UDP request from client
                DatagramPacket request = new DatagramPacket(readBuffer, QUOTE_LENGTH);
                socket.receive(request);

                String messageReceived = new String(request.getData());
                System.out.println("From client: " + messageReceived);

                String messageToSend = "Server received \"" + messageReceived + "\"";

                if (messageToSend.length() > QUOTE_LENGTH)
                    messageToSend = messageToSend.substring(0, QUOTE_LENGTH);

                writeBuffer = messageToSend.getBytes();

                InetAddress clientAddress = request.getAddress();
                int clientPort = request.getPort();

                readBuffer = new byte[QUOTE_LENGTH];

                // 3. send UDP reply to client
                DatagramPacket response = new DatagramPacket(
                    writeBuffer, 
                    writeBuffer.length,
                    clientAddress,
                    clientPort
                );
                socket.send(response);

                writeBuffer = new byte[QUOTE_LENGTH];

                if (messageReceived.endsWith(END_MESSAGE))
                    break;

            } catch (IOException ioException) {

                System.out.println(
                    "Rfc865UdpServer IOException: " + 
                    ioException.getMessage()
                );

                System.out.println(
                    "Stack Trace:\n" + 
                    ioException.getStackTrace()
                );
            } 
        }

        if (socket != null)
            socket.close();
    }
}
