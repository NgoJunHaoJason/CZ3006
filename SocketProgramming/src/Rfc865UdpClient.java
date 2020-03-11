import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

class Rfc865UdpClient {

    // quote of the day protocol

    private static final int PORT_NUMBER = 8001; // RFC865
    private static final int QUOTE_LENGTH = 512; // RFC865
    private static final String END_MESSAGE = "end";

    // buffer size of 2048 should be more than enough
    private static byte[] readBuffer = new byte[QUOTE_LENGTH];
    private static byte[] writeBuffer = new byte[QUOTE_LENGTH];

    public static void main(String[] args) {

        // 1. open UDP socket at well-known port
        DatagramSocket socket = null;

        try {
            socket = new DatagramSocket(PORT_NUMBER);

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

        try {
            String messageToSend = END_MESSAGE;

            if (messageToSend.length() > QUOTE_LENGTH)
                messageToSend = messageToSend.substring(0, QUOTE_LENGTH);

            writeBuffer = messageToSend.getBytes();

            // 2. send UDP request to server
            InetAddress serverAddress = InetAddress.getLocalHost();

            DatagramPacket request = new DatagramPacket(
                writeBuffer, 
                writeBuffer.length,
                serverAddress,
                8000 // server port
            );
            socket.send(request);

            writeBuffer = new byte[QUOTE_LENGTH];

            // 3. receive UDP reply from server
            DatagramPacket response = new DatagramPacket(readBuffer, QUOTE_LENGTH);
            socket.receive(response);

            String messageReceived = new String(request.getData());
            System.out.println("From server: " + messageReceived);

            readBuffer = new byte[QUOTE_LENGTH];

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

        if (socket != null)
            socket.close();
    }
}
