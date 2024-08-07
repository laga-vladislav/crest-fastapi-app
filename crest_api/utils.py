from urllib.parse import quote


def format_params(params, convention="%s"):
    if not params:
        return ""

    output = []
    for key, value in params.items():
        if isinstance(value, dict):
            output.append(format_params(value, convention % key + "[%s]"))
        elif isinstance(value, list):
            new_params = {str(i): element for i, element in enumerate(value)}
            output.append(format_params(new_params, convention % key + "[%s]"))
        else:
            key = quote(key)
            val = quote(str(value))
            output.append(convention % key + "=" + val)

    return "&".join(output)


def format_batch(calls) -> str:
    batch_params = []
    for i, call in enumerate(calls):
        method = call.get("method")
        params = call.get("params", {})
        formatted_params = format_params(params)
        batch_params.append(
            f"cmd[{i+1}]={quote(method + '?' + formatted_params)}")

    return "&".join(batch_params)
