from app.config.config import load_pipeline_configs



def main():
    pipeline_configs = load_pipeline_configs()
    print(f"pipeline configs: {pipeline_configs}")
    
main()