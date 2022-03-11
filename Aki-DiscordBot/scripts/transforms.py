
class TransformScripts():

    minute_rotation = {
        'm': '1',
        'h': '60',
        'd': '1440',
        'w': '10080',
    }

    second_rotation = {
        's': '1',
        'm': '60',
        'h': '3600',
        'd': '86400',
        'w': '604800',
    }

    @classmethod
    def transform_to_minute(self, time: str):
        alternative_time = ''
        for s in time:
            if s.lower() in self.minute_rotation:
                intermediate_time = self.minute_rotation[s.lower()] # Если такая буква есть, заносим её в новую переменную
            else:
                alternative_time += f'{s}'
        if int(alternative_time) <= 0:
            alternative_time = 1
        final_time = int(alternative_time) * int(intermediate_time)

        return final_time

    def test_transform_to_minute(self):
        print('======Minutes======')
        try:
            print(TransformScripts.transform_to_minute('10s'))
        except Exception as err:
            print(err)
        try:
            print(TransformScripts.transform_to_minute('10m'))
        except Exception as err:
            print(err)
        try:
            print(TransformScripts.transform_to_minute('10h'))
        except Exception as err:
            print(err)
        try:
            print(TransformScripts.transform_to_minute('10d'))
        except Exception as err:
            print(err)
        try:
            print(TransformScripts.transform_to_minute('10w'))
        except Exception as err:
            print(err)

    @classmethod
    def transform_to_seconds(self, time: str):
        alternative_time = ''
        for s in time:
            if s.lower() in self.second_rotation:
                intermediate_time = self.second_rotation[s.lower()] # Если такая буква есть, заносим её в новую переменную
            else:
                alternative_time += f'{s}'
        if int(alternative_time) <= 0:
            alternative_time = 1
        final_time = int(alternative_time) * int(intermediate_time)

        return final_time

    def test_transform_to_seconds(self):
        print('======Seconds======')
        try:
            print(TransformScripts.transform_to_seconds('10s'))
        except Exception as err:
            print(err)
        try:
            print(TransformScripts.transform_to_seconds('10m'))
        except Exception as err:
            print(err)
        try:
            print(TransformScripts.transform_to_seconds('10h'))
        except Exception as err:
            print(err)
        try:
            print(TransformScripts.transform_to_seconds('10d'))
        except Exception as err:
            print(err)
        try:
            print(TransformScripts.transform_to_seconds('10w'))
        except Exception as err:
            print(err)

if __name__ == '__main__':
    TransformScripts = TransformScripts()
    TransformScripts.test_transform_to_minute()
    TransformScripts.test_transform_to_seconds()