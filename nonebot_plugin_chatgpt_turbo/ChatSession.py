import openai


class ChatSession:
    def __init__(self, api_key, model_id, max_limit,org):
        self.api_key = api_key
        self.model_id = model_id
        self.content = []
        self.max_limit = max_limit
        self.org=org

    async def get_response(self, content, proxy):
        openai.api_key = self.api_key
        if proxy != "":
            openai.proxy = proxy
        if self.org != "":
            openai.organization = self.org

        try:
            self.content.append({"role": "user", "content": content})
            res_ = await openai.ChatCompletion.acreate(
                model=self.model_id,
                messages=self.content
            )

        except Exception as error:
            print(error)
            return

        use_prompt=int(res_.usage.prompt_tokens)
        use_completion=int(res_.usage.completion_tokens)
        price=use_prompt*0.03*0.001+use_completion*0.06*0.001

        res = res_.choices[0].message.content
        while res.startswith("\n") != res.startswith("？"):
            res = res[1:]

        self.content.append({"role": 'assistant', "content": res})

        while len(self.content) > 2*self.max_limit:
            self.content.pop(0)

        return res+f"\n---当前记忆条数{len(self.content)}/{2*self.max_limit}---\n---本次请求花费${round(price,5)}---"

    async def get_response2(self, content, proxy):
        openai.api_key = self.api_key
        if proxy != "":
            openai.proxy = proxy
        if self.org != "":
            openai.organization = self.org

        try:
            self.content.append({"role": "user", "content": content})
            res_ = await openai.ChatCompletion.acreate(
                model=self.model_id,
                messages=[{"role": "user", "content": content}]
            )

        except Exception as error:
            print(error)
            return
        
        use_prompt=int(res_.usage.prompt_tokens)
        use_completion=int(res_.usage.completion_tokens)
        price=use_prompt*0.03*0.001+use_completion*0.06*0.001

        res = res_.choices[0].message.content
        while res.startswith("\n") != res.startswith("？"):
            res = res[1:]

        self.content.append({"role": 'assistant', "content": res})
   

        while len(self.content) > 2*self.max_limit:
            self.content.pop(0)

        return res+f"\n---当前记忆条数{len(self.content)}/{2*self.max_limit}---\n---本次请求花费${round(price,5)}---"

