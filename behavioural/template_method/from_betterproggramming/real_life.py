# Imports etc...

class BitmexAPI:

    # Contructor etc...

    def place_order(self, order: Order):
        def place_order_api_call():
            size_sign = 1 if order.order_side == OrderSide.BUY else -1

            result = self.__bitmex_client.Order.Order_new(symbol='XBTUSD',
                                                          orderQty=size_sign * order.size,
                                                          price=order.price,
                                                          clOrdID=order.reference_key,
                                                          ordType='Limit').result()

            status_code = str(result[1])
            response_body = to_json(result[0])
            result_object = result[0]

            return status_code, response_body, result_object

        return self.__run_with_log(
            api_name='PLACE_ORDER_{}'.format(order.reference_key),
            api_call=place_order_api_call)

    def add_stop_loss(self, order: Order):
        def add_stop_loss_api_call():
            result = self.__bitmex_client.Order.Order_new(symbol='XBTUSD',
                                                          side=order.order_side.value,
                                                          clOrdID=order.reference_key,
                                                          ordType='Stop',
                                                          stopPx=order.price,
                                                          execInst='LastPrice,Close').result()

            status_code = str(result[1])
            response_body = to_json(result[0])
            result_object = result[0]

            return status_code, response_body, result_object

        return self.__run_with_log(
            api_name='ADD_STOP_LOSS_{}'.format(order.reference_key),
            api_call=add_stop_loss_api_call)

    def cancel_order_by_ref_key(self, ref_key: str):
        def cancel_order_api_call():
            result = self.__bitmex_client.Order.Order_cancel(
                clOrdID=ref_key).result()

            status_code = str(result[1])
            response_body = to_json(result[0][0])
            result_object = result[0][0]

            return status_code, response_body, result_object

        return self.__run_with_log(api_name='CANCEL_ORDER_{}'.format(ref_key),
                                   api_call=cancel_order_api_call)

    def __run_with_log(self, api_name, api_call, retry_count=0):
        time_of_call = datetime.now()
        status_code = ''
        error_message = ''
        concatenated_response_body = ''
        full_response_body = ''

        try:
            (status_code, response_message, result_object) = api_call()

            status_code = status_code
            full_response_body = response_message
            concatenated_response_body = response_message[:LOG_MESSAGE_LENGTH]

            return result_object

        except (HTTPTooManyRequests, HTTPServiceUnavailable) as e:
            status_code = str(e.response)
            error_message = str(e)[:LOG_MESSAGE_LENGTH]
            print('STATUS CODE: ', status_code)
            print('ERROR: ', error_message)
            if retry_count <= MAX_RETRY_COUNT:
                print('retry_count ({}) <= max_retry_count({})'.format(
                    retry_count, MAX_RETRY_COUNT))
                print('-> Sleeping for {} seconds and retrying'.format(
                    DURATION_BETWEEN_RETRIES))
                time.sleep(DURATION_BETWEEN_RETRIES)
                return self.__run_with_log(api_name=api_name,
                                           api_call=api_call,
                                           retry_count=retry_count + 1)
            else:
                print('retry_count ({}) > max_retry_count({})'.format(
                    retry_count, MAX_RETRY_COUNT))
                print('-> Throwing an error')
                status_code = str(e.response)
                error_message = str(e)[:LOG_MESSAGE_LENGTH]

                raise e


        except HTTPError as e:
            status_code = str(e.response)
            error_message = str(e)[:LOG_MESSAGE_LENGTH]

            raise e
        finally:
            print(
                '-------------------------------------API CALL BEGINNING----------------------------')
            print('API Name = ', api_name)
            print('Response Code = ', status_code)
            print('Api Executed at = ', time_of_call)

            if self.__with_verbose_logging:
                print()
                print('Full Response Body = ', full_response_body)
                print()
                print('Error Message = ', error_message)
            print(
                '-------------------------------------API CALL END---------------------------------')

            self.__log_service.log_api_call(vendor=self.__api_vendor_name,
                                            api_name=api_name,
                                            status_code=status_code,
                                            error_message=error_message,
                                            response_body=concatenated_response_body,
                                            time_of_call=time_of_call,
                                            caller=self.__caller)
