# Spring Boot Hello World (SSR + UI + Test)

## Run locally
Requires Java 17+ and Maven.

```bash
mvn spring-boot:run
```

Open: http://localhost:8080/hello

## Run tests
```bash
mvn test
```

## Debugging (proof)
Put a breakpoint inside `HelloController.hello()` and run the app in your IDE's Debug mode,
OR add a temporary log/print and show the output when hitting /hello.
