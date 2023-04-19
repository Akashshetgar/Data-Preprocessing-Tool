def pipeline_serializer(pipeline) -> dict:
    return {
        'id':str(pipeline["id"]),
        'pipeline_name':pipeline["pipeline_name"],
        'pipeline':pipeline["pipeline"]
       
    }


def pipelines_serializer(pipelines) -> list:
    return [pipeline_serializer(pipeline) for pipeline in pipelines] 