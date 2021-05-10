from ducts.event import EventHandler
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    async def setup(self, handler_spec, manager):
        self.evt_mturk_api_core = manager.get_handler_for(manager.key_ids["MTURK_API_CORE"])[1]
        self.evt_mturk_api_hit_core = manager.get_handler_for(manager.key_ids["MTURK_API_HIT_CORE"])[1]

        handler_spec.set_description('Creates HITs with a specified HIT type.')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        await self.evt_mturk_api_hit_core.create_hit_with_hit_type(**event.data or {})

    async def create_tutti_hit_batch(self, ProjectName, NumHITs, HITTypeParams, HITParams): 
        result = await self.evt_mturk_api_core.create_qualification_type(
                                    Name=f"TUTTI_HITTYPE_QUALIFICATION {dt}",
                                    Description="TUTTI_HITTYPE_QUALIFICATION",
                                    AutoGranted=False,
                                    QualificationTypeStatus="Active")
        qtid = result["QualificationType"]["QualificationTypeId"]

        HITTypeParams["QualificationRequirements"].append(dict(
                                    QualificationTypeId=qtid,
                                    Comparator="DoesNotExist",
                                    ActionsGuarded="DiscoverPreviewAndAccept"))

        result = await self.evt_mturk_api_core.create_hit_type(**HITTypeParams)
        HITParams["HITTypeId"] = result["HITTypeId"]

        # more like create_hit_with_hit_type_for_tutti_project
        result = await self.evt_mturk_api_hit_core.create_hit_with_hit_type(
                                    ProjectName=ProjectName,
                                    NumHITs=NumHITs,
                                    CreateHITsWithHITTypeParams=HITParams)

        output.set("Results", result)
