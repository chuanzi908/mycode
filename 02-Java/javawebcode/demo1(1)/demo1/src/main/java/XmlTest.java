import javax.xml.parsers.*;
import java.io.*;
import org.xml.sax.*;

public class XmlTest {
    public static void main(String[] args) throws Exception {
        String path = args[0];
        System.out.println("Parsing: " + path);
        System.out.println("File exists: " + new File(path).exists());
        System.out.println("File size: " + new File(path).length());

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setValidating(false);
        factory.setNamespaceAware(false);
        factory.setIgnoringComments(true);
        factory.setIgnoringElementContentWhitespace(false);
        factory.setCoalescing(false);
        factory.setExpandEntityReferences(true);

        DocumentBuilder builder = factory.newDocumentBuilder();
        builder.setEntityResolver(null);

        try {
            builder.parse(new File(path));
            System.out.println("XML parsed successfully!");
        } catch (SAXParseException e) {
            System.out.println("SAXParseException at line " + e.getLineNumber() + ", column " + e.getColumnNumber());
            System.out.println("Message: " + e.getMessage());
        }
    }
}