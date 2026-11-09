import javax.xml.parsers.*;
import java.io.*;
import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;
import javax.xml.XMLConstants;

public class XmlTest {
    public static void main(String[] args) throws Exception {
        String path = args[0];
        boolean validation = args.length > 1 && Boolean.parseBoolean(args[1]);
        
        System.out.println("Parsing: " + path);
        System.out.println("File exists: " + new File(path).exists());
        System.out.println("File size: " + new File(path).length());
        System.out.println("Validation: " + validation);

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
        factory.setValidating(validation);
        factory.setNamespaceAware(false);
        factory.setIgnoringComments(true);
        factory.setIgnoringElementContentWhitespace(false);
        factory.setCoalescing(false);
        factory.setExpandEntityReferences(true);

        DocumentBuilder builder = factory.newDocumentBuilder();
        builder.setEntityResolver(new EntityResolver() {
            public InputSource resolveEntity(String publicId, String systemId) {
                System.out.println("resolveEntity called: publicId=" + publicId);
                if ("-//mybatis.org//DTD Mapper 3.0//EN".equals(publicId) || 
                    "-//mybatis.org//DTD Config 3.0//EN".equals(publicId)) {
                    return new InputSource(new StringReader(""));
                }
                return null;
            }
        });
        builder.setErrorHandler(new DefaultHandler() {
            @Override
            public void error(SAXParseException exception) throws SAXException {
                System.out.println("[error] line=" + exception.getLineNumber() + " col=" + exception.getColumnNumber() + " msg=" + exception.getMessage());
            }
            @Override
            public void fatalError(SAXParseException exception) throws SAXException {
                System.out.println("[fatalError] line=" + exception.getLineNumber() + " col=" + exception.getColumnNumber() + " msg=" + exception.getMessage());
            }
            @Override
            public void warning(SAXParseException exception) throws SAXException {
                System.out.println("[warning] line=" + exception.getLineNumber() + " col=" + exception.getColumnNumber() + " msg=" + exception.getMessage());
            }
        });

        try {
            builder.parse(new File(path));
            System.out.println("XML parsed successfully!");
        } catch (SAXParseException e) {
            System.out.println("SAXParseException at line " + e.getLineNumber() + ", column " + e.getColumnNumber());
            System.out.println("Message: " + e.getMessage());
        }
    }
}