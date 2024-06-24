FROM openjdk:11-jre-slim

# WORKDIR /app
# COPY src/pom.xml ./pom.xml
# COPY src/src ./src

COPY src/target/java-grpc-server-1.0-SNAPSHOT-jar-with-dependencies.jar /app.jar

# RUN mvn clean package -DskipTests

# CMD ["java", "-jar", "/app/target/java-grpc-server-1.0-SNAPSHOT-jar-with-dependencies.jar"]
CMD ["java", "-jar", "/app.jar"]