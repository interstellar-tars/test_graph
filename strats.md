## Common Workflow Architecture

### Parallel

In a pure parallel workflow, all the jobs runs in parallel

```yaml
name: parallel
 
on: push
 
jobs:
  build:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
  test:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
  deploy:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
```

### Sequential

In a pure sequential workflow, all the jobs runs in series

```yaml
name: sequential
 
on: push
 
jobs:
  build:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
  unit-test:
   runs-on: ubuntu-latest
   needs: [build]
   steps:
     - run: echo "..."
  integration-test:
   runs-on: ubuntu-latest
   needs: [unit-test]
   steps:
     - run: echo "..."
  deploy:
   runs-on: ubuntu-latest
   needs: [integration-test]
   steps:
     - run: echo "..."
```

### Matrix Build and Test

```yaml
name: sequential
 
on: push
 
jobs:
  build:
   runs-on: ubuntu-latest
   strategy:
    matrix:
      os: [window,linux,mac]
   steps:
     - run: echo "..."
  unit-test:
   runs-on: ubuntu-latest
   strategy:
    matrix:
      node-version: [4,6,8]
   needs: [build]
   steps:
     - run: echo "..."
  integration-test:
   runs-on: ubuntu-latest
   needs: [unit-test]
   steps:
     - run: echo "..."
  deploy:
   runs-on: ubuntu-latest
   needs: [integration-test]
   steps:
     - run: echo "..."
```

### Fan-in-Fan-out

Fan-out flow is when multiple jobs are spawned in parallel once a single job or a group is completed. Fan-in flow is when a single job or a group waits for a multiple jobs to complete:

```yaml
name: fan-in-fan-out
 
on: push
 
jobs:
  build:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
  test-A-1:
   runs-on: ubuntu-latest
   needs: [build]
   steps:
     - run: echo "..."
  test-A-2:
   runs-on: ubuntu-latest
   needs: [test-A-1]
   steps:
     - run: echo "..."
  test-B:
   runs-on: ubuntu-latest
   needs: [build]
   steps:
     - run: echo "..." 
  test-C:
   runs-on: ubuntu-latest
   needs: [build]
   steps:
     - run: echo "..."
  integration-test:
   runs-on: ubuntu-latest
   needs: [test-A-2,test-B,test-C]
   steps:
     - run: echo "..."
  staging:
   runs-on: ubuntu-latest
   needs: [integration-test]
   steps:
     - run: echo "..."
  deploy:
   runs-on: ubuntu-latest
   needs: [staging]
   steps:
     - run: echo "..."
```
### Monorepo

In a monorepo workflow, you need to run multiple pipelines against multiple projects within a single repository. For instance, you can run pipelines for both Backend and Frontend in parallel.

```yaml
name: monorepo
 
on: push
 
jobs:
  backend-build:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
  frontend-build:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
  backend-lint:
   runs-on: ubuntu-latest
   needs: [backend-build]
   steps:
     - run: echo "..."
  frontend-lint:
   runs-on: ubuntu-latest
   needs: [frontend-build]
   steps:
     - run: echo "..."
  backend-test-A:
   runs-on: ubuntu-latest
   needs: [backend-lint]
   steps:
     - run: echo "..."
  backend-test-B:
   runs-on: ubuntu-latest
   needs: [backend-lint]
   steps:
     - run: echo "..."
  backend-test-C:
   runs-on: ubuntu-latest
   needs: [backend-lint]
   steps:
     - run: echo "..."
  frontend-test-A:
   runs-on: ubuntu-latest
   needs: [frontend-lint]
   steps:
     - run: echo "..."
  frontend-test-B:
   runs-on: ubuntu-latest
   needs: [frontend-lint]
   steps:
     - run: echo "..."
  e2e-test:
   runs-on: ubuntu-latest
   needs: [backend-test-A, backend-test-B, backend-test-C, frontend-test-A, frontend-test-A]
   steps:
     - run: echo "..."
  release-candidate:
   runs-on: ubuntu-latest
   needs: [e2e-test]
   steps:
     - run: echo "..."
  staging:
   runs-on: ubuntu-latest
   needs: [release-candidate]
   steps:
     - run: echo "..."
  deploy:
   runs-on: ubuntu-latest
   needs: [staging]
   steps:
     - run: echo "..."
```

### Multi-platform build

In a multi-platform build, you build and test your project against multiple platforms independently.

```yaml
name: multi-platform-build

on: push

jobs:
 ios-build:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
 android-build:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
 web-build:
   runs-on: ubuntu-latest
   steps:
     - run: echo "..."
 ios-test-A:
   runs-on: ubuntu-latest
   needs: [ios-build]
   steps:
     - run: echo "..."
 ios-test-B:
   runs-on: ubuntu-latest
   needs: [ios-build]
   steps:
     - run: echo "..."
 ios-test-C:
   runs-on: ubuntu-latest
   needs: [ios-build]
   steps:
     - run: echo "..."
 android-test-A:
   runs-on: ubuntu-latest
   needs: [android-build]
   steps:
     - run: echo "..."
 android-test-B:
   runs-on: ubuntu-latest
   needs: [android-build]
   steps:
     - run: echo "..."
 android-test-C:
   runs-on: ubuntu-latest
   needs: [android-build]
   steps:
     - run: echo "..."
 web-test-A:
   runs-on: ubuntu-latest
   needs: [web-build]
   steps:
     - run: echo "..."
 web-test-B:
   runs-on: ubuntu-latest
   needs: [web-build]
   steps:
     - run: echo "..."
 release:
   runs-on: ubuntu-latest
   needs: [ios-test-A,ios-test-B,ios-test-C,android-test-A,android-test-B,android-test-C,web-test-A,web-test-B]
   steps:
     - run: echo "..."
 ```

### Multi-ring deployment

In a multi-ring deployment, you progressively release/deploy your app to end users to limit the impact of change on end users and to continuously deliver value.

```yaml
name: multi-platform-build
 
on: push
 
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "..."

  lint:
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - run: echo "..."

  test-A:
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - run: echo "..."
    
  test-B:
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - run: echo "..."
 
  test-C:
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - run: echo "..."
 
  ring0-p1:
    runs-on: ubuntu-latest
    needs: [test-A,test-B,test-C]
    steps:
      - run: echo "..."

  ring0-p2:
    runs-on: ubuntu-latest
    needs: [test-A,test-B,test-C]
    steps:
      - run: echo "..."

  ring1-p1:
    runs-on: ubuntu-latest
    needs: [ring0-p1,ring0-p2]
    steps:
      - run: echo "..."

  ring1-p2:
    runs-on: ubuntu-latest
    needs: [ring0-p1,ring0-p2]
    steps:
      - run: echo "..."

  ring2-p1:
    runs-on: ubuntu-latest
    needs: [ring1-p1,ring1-p2]
    steps:
      - run: echo "..."

  ring2-p2:
    runs-on: ubuntu-latest
    needs: [ring1-p1,ring1-p2]
    steps:
      - run: echo "..."

  security-test:
    runs-on: ubuntu-latest
    needs: [ring2-p1,ring2-p2]
    steps:
      - run: echo "..."
 
  ring3-p1:
    runs-on: ubuntu-latest
    needs: [security-test]
    steps:
      - run: echo "..."

  ring4-p2:
    runs-on: ubuntu-latest
    needs: [security-test]
    steps:
      - run: echo "..."
```

### Child / Parent Pipelines

TBA


