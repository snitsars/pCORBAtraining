java -Xbootclasspath/a:collectionHelpers.jar -Djava.naming.factory.initial=com.sun.jndi.cosnaming.CNCtxFactory -Djava.naming.provider.url=iiop://localhost:8087 -cp .;%JUNIT_HOME%\junit.jar TestClient
