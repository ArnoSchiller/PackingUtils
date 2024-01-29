import matplotlib.pyplot as plt
from io import BytesIO
from fastapi import FastAPI, responses
from v1.models.bin_image_request_model import BinImageRequestModel

from packutils.visual.packing_visualization import PackingVisualization
from packutils.data.position import Position
from packutils.data.item import Item
from packutils.data.bin import Bin

import matplotlib

matplotlib.use("Agg")


api_v1 = FastAPI()


@api_v1.get("/")
async def status():
    return {"status": "Healthy"}


@api_v1.post(
    "/bin",
    # Set what the media type will be in the autogenerated OpenAPI specification.
    # fastapi.tiangolo.com/advanced/additional-responses/#additional-media-types-for-the-main-response
    responses={200: {"content": {"image/png": {}}}},
    # Prevent FastAPI from adding "application/json" as an additional
    # response media type in the autogenerated OpenAPI specification.
    # https://github.com/tiangolo/fastapi/issues/3258
    response_class=responses.Response,
)
def get_bin_image(request: BinImageRequestModel):
    vis = PackingVisualization()

    bin = Bin(
        width=request.colli_details.width,
        length=request.colli_details.length,
        height=request.colli_details.height,
    )

    errors = []
    for idx, p in enumerate(request.packages):
        done, msg = bin.pack_item(
            Item(
                id="",
                width=p.width,
                length=p.length,
                height=p.height,
                position=Position(x=p.x, y=p.y, z=p.z),
            )
        )
        if not done:
            errors.append(f"Failed to pack index {idx}: {msg}")

    if len(errors) == 0 and len(request.packages) != len(bin.packed_items):
        errors.append("Failed to pack each item")

    if len(errors) > 0:
        return responses.JSONResponse(status_code=422, content={"errors": errors})

    image = vis.visualize_bin(bin, show=False, return_png=False)

    # convert the image into bytes
    buffer = BytesIO()
    image.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return responses.StreamingResponse(buffer, media_type="image/png")