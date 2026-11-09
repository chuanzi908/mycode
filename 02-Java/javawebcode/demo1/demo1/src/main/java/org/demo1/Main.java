package org.demo1;

import org.apache.catalina.Context;
import org.apache.catalina.startup.Tomcat;

import java.io.File;

public class Main {
    public static void main(String[] args) throws Exception {
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(8080);
        tomcat.getConnector();

        File explodedDir = new File("target/demo1-1.0-SNAPSHOT");
        if (!explodedDir.exists()) {
            System.err.println("Exploded WAR directory not found: " + explodedDir.getAbsolutePath());
            System.err.println("Please run 'mvn package' first.");
            System.exit(1);
        }

        String webappDirPath = explodedDir.getAbsolutePath();
        System.out.println("Deploying from: " + webappDirPath);
        Context ctx = tomcat.addWebapp("", webappDirPath);

        tomcat.start();
        System.out.println("========================================");
        System.out.println("  Tomcat started: http://localhost:8080");
        System.out.println("========================================");
        tomcat.getServer().await();
    }
}