# IntelliJ Inspections Action

This is a [Github Action](https://github.com/features/actions) that runs [IntelliJ IDEA](https://www.jetbrains.com/idea/)’s [Code Inspections](https://www.jetbrains.com/help/idea/code-inspection.html), and comments on a PR with violations.

Please note that this action does not work on projects that already have an IDEA project. That is, your repository must not have the `.idea` folder checked in.

You should have the inspection profile in the root of your repository. It must be in a file named `Project_Default.xml`.

# Usage

Example usage in a workflow:

```yaml
name: CI

on: [pull_request]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
      with:
        lfs: true
    - name: Set up JDK 1.8
      uses: actions/setup-java@v1
      with:
        java-version: 1.8
    - name: Gradle tests
      run: ./gradlew clean check
    - name: Run IntelliJ Inspections
      uses: gps/intellij-inspections-action@master
      with:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    - name: Save inspection results
      uses: actions/upload-artifact@v1
      if: always()
      with:
        name: idea_inspections
        path: target/idea_inspections
```
