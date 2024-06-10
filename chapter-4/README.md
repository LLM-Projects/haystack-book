# Reliable AI

As the chapter name suggests we need to ensure that our RAG Application is a safe place for everyone. In that case, there has to be a mechanism to track the responses so that we can keep an eye on the output being generated. This will give us the power to fine tune our pipeline and restrict the model to generate much safer, consistent, and relevant results.

To overcome the pain points listed above haystack provides us with two solutions namely [logging](https://docs.haystack.deepset.ai/docs/logging) and [tracing](https://docs.haystack.deepset.ai/docs/tracing). 

## Logging
[Logging](https://docs.python.org/3/library/logging.html) is very useful during the building phase of the pipeline or the application on the whole. It gives full control to the developer to understand flow of the program. We can log different levels based on the requirement. Widely used tracking levels are error capturing, code debugger, or full conrtol over the working. We can alter the logger level and get the desired results.

Various logging [levels](https://docs.python.org/3/library/logging.html#logging-levels) for reference:
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

P.S. Each level has numeric value associated with the base value 10 and the remaining increasing by 10 in top down order.

## Tracing
Tracing comes handy especially when we need to find which part of the code/pipeline is causing the error or producing the unexpected results. Multiple tracing solutions include:
- OpenTelemetry and Jaeger
- Langfuse

### OpenTelemetry and Jaegar
For this we make use of [OpenTelemetry](https://docs.haystack.deepset.ai/docs/tracing#opentelemetry) to trace our RAG application. The UI is rendered using Jaeger.

By running the script below we are done with setting up the Jaeger UI which can be accessed in `localhost` port `16686`.

```bash
docker run --rm -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1
```

This produces almost all the details required to debug the cause of the event by ensuring to track the necessary indicators with appealing visualizations.

### Langfuse
Another tracing solution is langfuse. It's main advantage is that this is cloud based. You need to setup the environment variables and then you are all set to start. Finally, to haystack to recognize we need to add this component to the pipeline. It doesn't need to be connected to any other component.
Then we can track the runs in the Langfuse dashboard.

## Custom Component (Prompt Injection)
In Reliable AI, we need to ensure that prompts aren't manipulated. So to ensure that the prompts are safe and not manipulated we make use of the pretrained models from Huggingface as a component. This showcases how we can ensure a reliable response from LLM and at the same time showcase the power of haystack custom component feature to flexibly integrate anything into a pipeline.

**Most common position in a pipeline**: After the [PromptBuilder](https://docs.haystack.deepset.ai/docs/promptbuilder) component
**Mandatory input variables**: `prompt_input` : string
**Output variables**: `safe` and `injection` : Floating values
