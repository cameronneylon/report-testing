Reporting tool intended to facilitate automated and reproducible reports.

## Orientation

The system runs in two discrete stages.

### Stage One: Data Analysis

This step runs user-specified functions which perform all necessary data analysis and generate any desired plots or charts. Any statistics, data tables, images, or other calculable aspects of the reporting should be generated by calling python scripts. (Non-python analysis can be supported by having python scripts which launch other processes.)

### Stage Two: Document Preparation

After stage one, there should be a variety of assets generated, ready for inclusion in a document. In Stage Two, the document template is first processed through the Jinja2 templating system, which allows assets to be referenced by name, and have their value (as calculated in Stage One), be inserted into the document.

Document templates are in Markdown by default, but can be provided in a variety of text-based formats. Once the template has been rendered, further filters can be applied to convert the document into a variety of final formats.

## Details

### Caching

As some calculations may be very computationally intensive, we don't want to re-do them if nothing has changed. We also want to be able to quickly iterate on our final document, for example to tweak wording or layout. On the other hand, we don't want to risk including incorrect or out-of-date versions of plots or data points.

For every function which is run, we generate a hashcode based on a number of attributes. If any of these attributes change, we assume the function is out of date. Attributes include the source code of the function, arguments passed to the function, and the source code of the reporting system itself. The first time a function is run, metadata is saved and stored in a JSON file in a google cloud storage bucket. When a function is run subsequently, the system looks for a file matching the hashcode of the function attributes. If present, then we'll download the stored metadata and any referenced asset files.

There is not sophisticated dependency management with this system, so it is better to avoid invisiblie side-effects between functions as this may result in inconsistent state.

